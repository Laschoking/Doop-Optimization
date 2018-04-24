package org.clyze.doop.wala;

import com.ibm.wala.analysis.typeInference.TypeAbstraction;
import com.ibm.wala.analysis.typeInference.TypeInference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IField;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.AnalysisCacheImpl;
import com.ibm.wala.ipa.callgraph.AnalysisOptions;
import com.ibm.wala.ipa.callgraph.IAnalysisCacheView;
import com.ibm.wala.ipa.callgraph.impl.Everywhere;
import com.ibm.wala.shrikeCT.InvalidClassFileException;
import com.ibm.wala.ssa.*;
import com.ibm.wala.types.TypeReference;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import soot.ArrayType;
import soot.RefLikeType;
import soot.RefType;
import soot.Type;

import java.util.Iterator;
import java.util.Set;

/**
 * Traverses Soot classes and invokes methods in FactWriter to
 * generate facts. The class FactGenerator is the parseParamsAndRun class
 * controlling what facts are generated.
 */

class WalaFactGenerator implements Runnable {

    protected Log logger;

    private WalaFactWriter _writer;
    private Set<IClass> _iClasses;
    private AnalysisOptions options;
    private IAnalysisCacheView cache;
    private WalaIRPrinter IRPrinter;

    WalaFactGenerator(WalaFactWriter writer, Set<IClass> iClasses, String outDir)
    {
        this._writer = writer;
        this.logger = LogFactory.getLog(getClass());
        this._iClasses = iClasses;
        options = new AnalysisOptions();
        options.getSSAOptions().setPiNodePolicy(SSAOptions.getAllBuiltInPiNodes()); //CURRENTLY these are not active
        cache = new AnalysisCacheImpl();                //Without the SSaOptions -- piNodes
        //cache = new AnalysisCacheImpl(new DefaultIRFactory(), options.getSSAOptions()); //Change to this to make the IR according to the SSAOptions -- to include piNodes
        IRPrinter = new WalaIRPrinter(cache,outDir);
    }


    @Override
    public void run() {

        for (IClass iClass : _iClasses) {
            IRPrinter.printIR(iClass);

            _writer.writeClassOrInterfaceType(iClass);
            //TODO: Handling of Arrays?
            if(iClass.isAbstract())
                _writer.writeClassModifier(iClass, "abstract");
//            if(Modifier.isFinal(modifiers))
//                _writer.writeClassModifier(iClass, "final");
            if(iClass.isPublic())
                _writer.writeClassModifier(iClass, "public");
            if(iClass.isPrivate())
                _writer.writeClassModifier(iClass, "private");

            // the isInterface condition prevents Object as superclass of interface
            if (iClass.getSuperclass() != null && !iClass.isInterface()) {
                _writer.writeDirectSuperclass(iClass, iClass.getSuperclass());
            }

            for (IClass i : iClass.getAllImplementedInterfaces()) {
                _writer.writeDirectSuperinterface(iClass, i);
            }

            iClass.getDeclaredInstanceFields().forEach(this::generate);
            iClass.getDeclaredStaticFields().forEach(this::generate);

            for (IMethod m : iClass.getDeclaredMethods()) {
                Session session = new org.clyze.doop.wala.Session();
                try {
                    generate(m, session);
                }
                catch (Exception exc) {
                    System.err.println("Error while processing method: " + m + " of class " +m.getDeclaringClass());
                    exc.printStackTrace();
                    throw exc;
                }
            }
        }
    }

    private void generate(IField f)
    {
        _writer.writeField(f);
        _writer.writeFieldInitialValue(f); //TODO: Fix this

        if(f.isFinal())
            _writer.writeFieldModifier(f, "final");
        if(f.isPrivate())
            _writer.writeFieldModifier(f, "private");
        if(f.isProtected())
            _writer.writeFieldModifier(f, "protected");
        if(f.isPublic())
            _writer.writeFieldModifier(f, "public");
        if(f.isStatic())
            _writer.writeFieldModifier(f, "static");
//        if(Modifier.isSynchronized(modifiers))
//            _writer.writeFieldModifier(f, "synchronized");
//        if(Modifier.isTransient(modifiers))
//            _writer.writeFieldModifier(f, "transient");
        if(f.isVolatile())
            _writer.writeFieldModifier(f, "volatile");
        // TODO interface?
        // TODO strictfp?
        // TODO annotation?
        // TODO enum?
    }

    private void generate(IMethod m, Session session)
    {
        _writer.writeMethod(m);
        if(m.isAbstract())
            _writer.writeMethodModifier(m, "abstract");
        if(m.isFinal())
            _writer.writeMethodModifier(m, "final");
        if(m.isNative())
            _writer.writeMethodModifier(m, "native");
        if(m.isPrivate())
            _writer.writeMethodModifier(m, "private");
        if(m.isProtected())
            _writer.writeMethodModifier(m, "protected");
        if(m.isPublic())
            _writer.writeMethodModifier(m, "public");
        if(m.isStatic())
            _writer.writeMethodModifier(m, "static");
        if(m.isSynchronized())
            _writer.writeMethodModifier(m, "synchronized");
        // TODO would be nice to have isVarArgs in Wala
//        if(Modifier.isTransient(modifiers))
//            _writer.writeMethodModifier(m, "varargs");
        if(m.isSynchronized())
            _writer.writeMethodModifier(m, "volatile");
        if(m.isSynthetic())
            _writer.writeMethodModifier(m, "synthetic");
        if(m.isBridge())
            _writer.writeMethodModifier(m, "bridge");

        if(m.isNative())
        {
            _writer.writeNativeReturnVar(m);
        }
        int paramIndex = 0;
        if(!m.isStatic())
        {
            _writer.writeThisVar(m);
            paramIndex = 1;
        }

        while (paramIndex < m.getNumberOfParameters()) {
            if (m.isStatic() || m.isClinit()) {
                _writer.writeFormalParam(m, paramIndex, paramIndex);
            }
            else {
                _writer.writeFormalParam(m, paramIndex, paramIndex - 1);
            }
            paramIndex++;
        }

        try {
            for(TypeReference exceptionType: m.getDeclaredExceptions())
            {
                _writer.writeMethodDeclaresException(m, exceptionType);
            }
        } catch (InvalidClassFileException e) {
            e.printStackTrace();
        }

        if(!(m.isAbstract() || m.isNative()))
        {
            IR ir = cache.getIR(m, Everywhere.EVERYWHERE);
            generate(m, ir, session);
        }
    }

    private void generate(IMethod m, IR ir, Session session)
    {

        SSAInstruction[] instructions = ir.getInstructions();
        SSACFG cfg = ir.getControlFlowGraph();
        TypeInference typeInference = TypeInference.make(ir,true); // Not sure about true for doPrimitives
        SSACFG.ExceptionHandlerBasicBlock previousHandlerBlock = null;
        for (int i = 0; i <= cfg.getMaxNumber(); i++) {
            SSACFG.BasicBlock basicBlock = cfg.getNode(i);
            int start = basicBlock.getFirstInstructionIndex();
            int end = basicBlock.getLastInstructionIndex();

            Iterator<SSAPhiInstruction> phis = basicBlock.iteratePhis();
            while(phis.hasNext())
            {
                SSAPhiInstruction phiInstruction = phis.next();
                generate(m, ir, phiInstruction, session, typeInference);
            }
            for (int j = start; j <= end; j++) {
                if (instructions[j] != null) {
                    this.generateDefs(m, ir, instructions[j], session, typeInference);
                    this.generateUses(m, ir, instructions[j], session, typeInference);

                    if (instructions[j] instanceof SSAReturnInstruction) {
                        generate(m, ir, (SSAReturnInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSABinaryOpInstruction) {
                        generate(m, ir, (SSABinaryOpInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAMonitorInstruction) {
                        generate(m, ir, (SSAMonitorInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAThrowInstruction) {
                        generate(m, ir, (SSAThrowInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAInvokeInstruction) {
                        generate(m, ir, (SSAInvokeInstruction) instructions[j], session,typeInference);
                    }
                    else if (instructions[j] instanceof SSAGetInstruction) {
                        generate(m, ir, (SSAGetInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAPutInstruction) {
                        generate(m, ir, (SSAPutInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAUnaryOpInstruction) {
                        generate(m, ir, (SSAUnaryOpInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAArrayLengthInstruction) {
                        generate(m, ir, (SSAArrayLengthInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAArrayLoadInstruction) {
                        generate(m, ir, (SSAArrayLoadInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAArrayStoreInstruction) {
                        generate(m, ir, (SSAArrayStoreInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSANewInstruction) {
                        generate(m, ir, (SSANewInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAPhiInstruction) {
                        //SSAPhiInstructions are not stored in instructions[]
                    }
                    else if (instructions[j] instanceof SSAPiInstruction) { //TODO:Figure out what this does
                        //SSAPiInstructions are not stored in instructions[]
                    }
                    else if (instructions[j] instanceof SSAGetCaughtExceptionInstruction) {
                        //SSAGetCaughtExceptionInstructions are not stored in instructions[]
                    }
                    else if (instructions[j] instanceof SSAComparisonInstruction) {
                        generate(m, ir, (SSAComparisonInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSALoadMetadataInstruction) {
                        generate(m, ir, (SSALoadMetadataInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAAddressOfInstruction) {
                        System.out.println("Impossible!");
                    }
                    else if (instructions[j] instanceof SSAStoreIndirectInstruction) {
                        System.out.println("Impossible vol2!");
                    }
                    else if (instructions[j] instanceof SSALoadIndirectInstruction) {
                        System.out.println("Impossible vol3!");
                    }
                    else if (instructions[j] instanceof SSASwitchInstruction) {
                        //generate(m, ir, (SSASwitchInstruction) instructions[j], session, typeInference);
                        session.calcInstructionNumber(instructions[j]);
                    }
                    else if (instructions[j] instanceof SSAGotoInstruction) {
                        //generate(m, ir, (SSAGotoInstruction) instructions[j], session);
                        session.calcInstructionNumber(instructions[j]);
                    }
                    else if (instructions[j] instanceof SSAConditionalBranchInstruction) {
                        //generate(m, ir, (SSAConditionalBranchInstruction) instructions[j], session, typeInference);
                        session.calcInstructionNumber(instructions[j]);
                    }
                    else if (instructions[j] instanceof SSAInstanceofInstruction) {
                        generate(m, ir, (SSAInstanceofInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSACheckCastInstruction) {
                        generate(m, ir, (SSACheckCastInstruction) instructions[j], session, typeInference);
                    }
                    else if (instructions[j] instanceof SSAConversionInstruction) {
                        generate(m, ir, (SSAConversionInstruction) instructions[j], session, typeInference);
                    }
                }
            }

            Iterator<SSAPiInstruction> pis = basicBlock.iteratePis();
            while(pis.hasNext())
            {
                SSAPiInstruction piInstruction = pis.next();

            }


            if (basicBlock instanceof SSACFG.ExceptionHandlerBasicBlock) {
                //System.out.println("method " + m.getName() + " in class " + m.getDeclaringClass().toString() + " Exc handling block " + start + " " + end);
                if(((SSACFG.ExceptionHandlerBasicBlock) basicBlock).getCatchInstruction() == null )
                {
                    //System.out.println(" NULL CATCH INSTRUCTION");
                    continue;
                }
                //System.out.println( ((SSACFG.ExceptionHandlerBasicBlock) basicBlock).getCatchInstruction().toString(ir.getSymbolTable()) + " with iindex " +((SSACFG.ExceptionHandlerBasicBlock) basicBlock).getCatchInstruction().iindex);

//                for (int j = start; j <= end; j++)
//                    if (instructions[j] != null)
//                        System.out.println( instructions[j].toString(ir.getSymbolTable()));
//                    else
//                        System.out.println( "Instuction "+j + " is null :(");
                if (previousHandlerBlock != null)
                    _writer.writeExceptionHandlerPrevious(m, (SSACFG.ExceptionHandlerBasicBlock)basicBlock, previousHandlerBlock, session);
                _writer.writeExceptionHandler(ir, m ,(SSACFG.ExceptionHandlerBasicBlock)basicBlock,session, typeInference);
                previousHandlerBlock = (SSACFG.ExceptionHandlerBasicBlock) basicBlock;
            }
        }

        for (int i = 0; i <= cfg.getMaxNumber(); i++) {
            SSACFG.BasicBlock basicBlock = cfg.getNode(i);
            int start = basicBlock.getFirstInstructionIndex();
            int end = basicBlock.getLastInstructionIndex();

            for (int j = start; j <= end; j++) {
                if (instructions[j] instanceof SSASwitchInstruction) {
                    generate(m, ir, (SSASwitchInstruction) instructions[j], session, typeInference);
                } else if (instructions[j] instanceof SSAGotoInstruction) {
                    generate(m, ir, (SSAGotoInstruction) instructions[j], session);
                } else if (instructions[j] instanceof SSAConditionalBranchInstruction) {
                    generate(m, ir, (SSAConditionalBranchInstruction) instructions[j], session, typeInference);
                }
            }
        }
    }

    /*
     * From what I understand all SSASwitchInsutrctions are LookUp Switches in WALA
     * This transformation takes place in com.ibm.wala.shrikeBT.Decoder.java
     * In constrast soot has both LookUp Switches and Table Switches
     */
    public void generate(IMethod m, IR ir, SSASwitchInstruction instruction, Session session, TypeInference typeInference) {
        //Switch instructions have only one use
        Local switchVar =createLocal(ir,instruction,instruction.getUse(0),typeInference);
        _writer.writeLookupSwitch(ir, m, instruction, session, switchVar);

    }
    public void generate(IMethod m, IR ir, SSAConditionalBranchInstruction instruction, Session session, TypeInference typeInference) {
        SSAInstruction[] ssaInstructions = ir.getInstructions();

        // Conditional branch instructions have two uses (op1 and op2, the compared variables) and no defs
        Local op1 = createLocal(ir, instruction, instruction.getUse(0), typeInference);
        Local op2 = createLocal(ir, instruction, instruction.getUse(1), typeInference);

        if(ssaInstructions[instruction.getTarget()] == null) {
            int nextWALAIndex = getNextNonNullInstruction(ir,instruction.getTarget());
            if(nextWALAIndex == -1)
                logger.error("Error: Next non-null instruction index = -1");
            _writer.writeIf(m, instruction, op1, op2, ssaInstructions[nextWALAIndex], session);
        }
        else
            _writer.writeIf(m, instruction, op1, op2, ssaInstructions[instruction.getTarget()], session);
    }


    public void generate(IMethod m, IR ir, SSAPhiInstruction instruction, Session session, TypeInference typeInference) {
        // Phi instructions have a single def (to) and a number uses that represent the alternative values
        Local to = createLocal(ir, instruction, instruction.getDef(), typeInference);
        Local alternative;
        for(int i=0; i < instruction.getNumberOfUses();i++)
        {
            if (instruction.getUse(i) > -1) {
                alternative = createLocal(ir, instruction, instruction.getUse(i), typeInference);
            }
            else {
                continue;
            }
            _writer.writeAssignLocal(m, instruction, to, alternative, session);
        }
    }

    public void generate(IMethod m, IR ir, SSANewInstruction instruction, Session session, TypeInference typeInference) {
        Local l = createLocal(ir,instruction,instruction.getDef(),typeInference);
        int numOfUses = instruction.getNumberOfUses();
        if(numOfUses < 2)
        {
            _writer.writeAssignHeapAllocation(ir, m, instruction, l, session);
        }
        else
        {
            _writer.writeAssignNewMultiArrayExpr(m, instruction, l, session);
        }
    }

    public void generate(IMethod m, IR ir, SSALoadMetadataInstruction instruction, Session session, TypeInference typeInference) {
        session.calcInstructionNumber(instruction);//TODO: Move this when method is implemented

    }

    public void generate(IMethod m, IR ir, SSAArrayLoadInstruction instruction, Session session, TypeInference typeInference) {
        // Load array instructions have a single def (to) and two uses (base and index);
        Local to = createLocal(ir, instruction, instruction.getDef(), typeInference);
        Local base = createLocal(ir, instruction, instruction.getUse(0), typeInference);
        Local index = createLocal(ir, instruction, instruction.getUse(1), typeInference);

        _writer.writeLoadArrayIndex(m, instruction, base, to, index, session);
    }

    public void generate(IMethod m, IR ir, SSAArrayStoreInstruction instruction, Session session, TypeInference typeInference) {
        // Store arra instructions have three uses (base, index and from) and no defs
        Local base = createLocal(ir, instruction, instruction.getUse(0), typeInference);
        Local index = createLocal(ir, instruction, instruction.getUse(1), typeInference);
        Local from = createLocal(ir, instruction, instruction.getUse(2), typeInference);

        _writer.writeStoreArrayIndex(m, instruction, base, from, index, session);
    }

    public void generate(IMethod m, IR ir, SSAGetInstruction instruction, Session session, TypeInference typeInference) {
        Local to = createLocal(ir, instruction, instruction.getDef(), typeInference);

        if (instruction.isStatic()) {
            //Get static field has no uses and a single def (to)
            _writer.writeLoadStaticField(m, instruction, instruction.getDeclaredField(), to, session);
        }
        else {
            //Get instance field has one use (base) and one def (to)
            Local base = createLocal(ir, instruction, instruction.getUse(0), typeInference);
            _writer.writeLoadInstanceField(m, instruction, instruction.getDeclaredField(), base, to, session);
        }
    }

    public void generate(IMethod m, IR ir, SSAPutInstruction instruction, Session session, TypeInference typeInference) {

        if (instruction.isStatic()) {
            //Put static field has a single use (from) and no defs
            Local from = createLocal(ir, instruction, instruction.getUse(0), typeInference);
            _writer.writeStoreStaticField(m, instruction, instruction.getDeclaredField(), from, session);
        }
        else {
            //Put instance field has two uses (base and from) and no defs
            Local base = createLocal(ir, instruction, instruction.getUse(0), typeInference);
            Local from = createLocal(ir, instruction, instruction.getUse(1), typeInference);
            _writer.writeStoreInstanceField(m, instruction, instruction.getDeclaredField(), base, from, session);
        }
    }

    public void generate(IMethod m, IR ir, SSAInvokeInstruction instruction, Session session, TypeInference typeInference) {
        // For invoke instructions the number of uses is equal to the number of parameters

        Local l;
        if(instruction.getNumberOfReturnValues() == 0)
            l = null;
        else
            l = createLocal(ir, instruction, instruction.getDef(), typeInference);
        _writer.writeInvoke(m, ir, instruction, l, session,typeInference);
    }

    public void generate(IMethod m, IR ir, SSAInstanceofInstruction instruction, Session session, TypeInference typeInference) {
        // For invoke instructions the number of uses is equal to the number of parameters
        Local to = createLocal(ir, instruction, instruction.getDef(), typeInference);
        Local from = createLocal(ir, instruction, instruction.getUse(0), typeInference);
        _writer.writeAssignInstanceOf(m,  instruction, to, from,instruction.getCheckedType(), session);
    }

    //SSACheckCastInstruction is for non primitive types
    public void generate(IMethod m, IR ir, SSACheckCastInstruction instruction, Session session, TypeInference typeInference) {
        // For invoke instructions the number of uses is equal to the number of parameters
        Local to =createLocal(ir, instruction, instruction.getDef(), typeInference);
        Local from = createLocal(ir, instruction, instruction.getUse(0), typeInference);
        TypeReference[] types = instruction.getDeclaredResultTypes();
        if(types.length!=1)
        {
            logger.debug("Instruction: " + instruction.toString(ir.getSymbolTable()));
            for(TypeReference type:types)
                logger.debug("Checkcast type is " + type.toString());
        }
        for(TypeReference type:types) {
            if(ir.getSymbolTable().isStringConstant(instruction.getUse(0)) || ir.getSymbolTable().isNullConstant(instruction.getUse(0)))//TODO:No class constant?
                _writer.writeAssignCastNull(m,instruction,to,type,session);
            else
                _writer.writeAssignCast(m, instruction, to, from, type, session);
        }
    }

    //SSAConversion Instruction is only for primitive types
    public void generate(IMethod m, IR ir, SSAConversionInstruction instruction, Session session, TypeInference typeInference) {
        // For invoke instructions the number of uses is equal to the number of parameters
        Local to =createLocal(ir, instruction, instruction.getDef(), typeInference);
        Local from = createLocal(ir, instruction, instruction.getUse(0), typeInference);

        if(ir.getSymbolTable().isNumberConstant(instruction.getUse(0)) )
            _writer.writeAssignCastNumericConstant(m, instruction, to, from , instruction.getToType(), session);
        else
            _writer.writeAssignCast(m, instruction, to, from , instruction.getToType(), session);
    }

    public void generate(IMethod m, IR ir, SSAGotoInstruction instruction, Session session) {
        // Go to instructions have no uses and no defs
        SSAInstruction[] ssaInstructions = ir.getInstructions();
        if(ssaInstructions[instruction.getTarget()] == null) {
            int nextWALAIndex = getNextNonNullInstruction(ir,instruction.getTarget());
            if(nextWALAIndex == -1)
                logger.error("Error: Next non-null instruction index = -1");
            _writer.writeGoto(m, instruction, ssaInstructions[nextWALAIndex], session);
        }
        else
            _writer.writeGoto(m, instruction,ssaInstructions[instruction.getTarget()] , session);
    }

    public void generate(IMethod m, IR ir, SSAMonitorInstruction instruction, Session session, TypeInference typeInference) {
        // Monitor instructions have a single use and no defs
        int use = instruction.getUse(0);
        Local l = createLocal(ir, instruction, use, typeInference);
        if (instruction.isMonitorEnter()) {
            _writer.writeEnterMonitor(m, instruction, l, session);
        }
        else {
            _writer.writeExitMonitor(m, instruction, l, session);
        }
    }

    public void generate(IMethod m, IR ir, SSAUnaryOpInstruction instruction, Session session, TypeInference typeInference) {
        // Unary op instructions have a single def (to) and a single use (from)
        Local to = createLocal(ir, instruction, instruction.getDef(), typeInference);
        Local from = createLocal(ir, instruction, instruction.getUse(0), typeInference);

        _writer.writeAssignUnop(m, instruction, to, from, session);
    }

    public void generate(IMethod m, IR ir, SSAArrayLengthInstruction instruction, Session session, TypeInference typeInference) {
        // Array length instruction have a single use (base) and a def (to)
        Local to = createLocal(ir, instruction, instruction.getDef(), typeInference);
        Local base = createLocal(ir, instruction, instruction.getUse(0), typeInference);

        _writer.writeAssignArrayLength(m, instruction, to, base, session);
    }

    private Local createLocal(IR ir, SSAInstruction instruction, int varIndex, TypeInference typeInference) {
        Local l;

        TypeReference typeRef;
        TypeAbstraction typeAbstraction = typeInference.getType(varIndex);
        if (typeAbstraction == null) {                    // anantoni: TypeAbstraction == null means undefined type
            typeRef = TypeReference.JavaLangObject;
        }
        else {                                            // All other cases - including primitives - should be handled by getting the TypeReference
            typeRef = typeAbstraction.getTypeReference();
            if (typeRef == null) {                        // anantoni: In this case we have encountered WalaTypeAbstraction.TOP
                typeRef = TypeReference.JavaLangObject;   // TODO: we don't know what type to give for TOP
            }
        }
        if(ir.getMethod().getName().toString().equals("nothing"))System.out.println("type is " + typeRef.toString());
        if (instruction.iindex != -1) {
            String[] localNames = ir.getLocalNames(instruction.iindex, varIndex);
            if (localNames != null) {

                l = new Local("v" + varIndex, varIndex, localNames[0], typeRef);
            }
            else {
                l = new Local("v" + varIndex, varIndex, typeRef);
            }
        }
        else {
            l = new Local("v" + varIndex, varIndex, typeRef);
        }
        if(ir.getSymbolTable().isConstant(varIndex) && ! ir.getSymbolTable().isNullConstant(varIndex))
            l.setValue(ir.getSymbolTable().getConstantValue(varIndex).toString());

        return l;
    }

    /**
     * Return statement
     */
    private void generate(IMethod m, IR ir, SSAReturnInstruction instruction, Session session, TypeInference typeInference)
    {
        if (instruction.returnsVoid()) {
            // Return void has no uses
            _writer.writeReturnVoid(m, instruction, session);
        }
        else {
            // Return something has a single use
            Local l = createLocal(ir, instruction, instruction.getUse(0), typeInference);
            l.type = m.getReturnType();
            _writer.writeReturn(m, instruction, l, session);
        }
    }

    private void generateDefs(IMethod m, IR ir, SSAInstruction instruction, Session session, TypeInference typeInference) {
        SymbolTable symbolTable = ir.getSymbolTable();

        if (instruction.hasDef()) {
            for (int i = 0; i < instruction.getNumberOfDefs(); i++) {
                int def = instruction.getDef(i);
                Local l = createLocal(ir, instruction, def, typeInference);
                if (def != 1 && symbolTable.isConstant(def)) {
                    Value v = symbolTable.getValue(def);
                    generateConstant(m, ir, instruction, v, l, session);
                } else {
                    _writer.writeLocal(m, l);
                }
            }
        }
    }

    private void generateUses(IMethod m, IR ir, SSAInstruction instruction, Session session, TypeInference typeInference) {
        SymbolTable symbolTable = ir.getSymbolTable();

        for (int i = 0; i < instruction.getNumberOfUses(); i++) {
            int use = instruction.getUse(i);
            Local l = createLocal(ir, instruction, use, typeInference);
            if (use != -1 && symbolTable.isConstant(use)) {
                Value v = symbolTable.getValue(use);
                generateConstant(m, ir, instruction, v, l, session);
                if(m.getName().toString().equals("nothing"))System.out.println("var v"+use + " is constant.");
            }
        }
    }

    private void generateConstant(IMethod m, IR ir, SSAInstruction instruction, Value v, Local l, Session session) {
        SymbolTable symbolTable = ir.getSymbolTable();

        String s = v.toString();
        if (v.isStringConstant()) {
            l.setType(TypeReference.JavaLangString);
            _writer.writeStringConstantExpression(m, instruction, l, (ConstantValue) v, session);
        } else if (v.isNullConstant()) {
            _writer.writeNullExpression(m, instruction, l, session);
        } else if (symbolTable.isIntegerConstant(l.getVarIndex())) {
            l.setType(TypeReference.Int);
            _writer.writeNumConstantExpression(m, instruction, l, (ConstantValue) v, session);
        } else if (symbolTable.isLongConstant(l.getVarIndex())) {
            l.setType(TypeReference.Long);
            _writer.writeNumConstantExpression(m, instruction, l, (ConstantValue) v, session);
        } else if (symbolTable.isFloatConstant(l.getVarIndex())) {
            l.setType(TypeReference.Float);
            _writer.writeNumConstantExpression(m, instruction, l, (ConstantValue) v, session);
        } else if (symbolTable.isDoubleConstant(l.getVarIndex())) {
            l.setType(TypeReference.Double);
            _writer.writeNumConstantExpression(m, instruction, l, (ConstantValue) v, session);
        } else if (symbolTable.isBooleanConstant(l.getVarIndex())) {
            l.setType(TypeReference.Boolean);
            _writer.writeNumConstantExpression(m, instruction, l, (ConstantValue) v, session);
        } else if (s.startsWith("#[") || (s.startsWith("#L") && s.endsWith(";"))) {
            _writer.writeClassConstantExpression(m, instruction, l, (ConstantValue) v, session);
        }
    }

    private void generate(IMethod m, IR ir, SSABinaryOpInstruction instruction, Session session, TypeInference typeInference)
    {
        // Binary instructions have two uses and a single def
        Local l = createLocal(ir, instruction, instruction.getDef(), typeInference);
        Local op1 = createLocal(ir, instruction, instruction.getUse(0), typeInference);
        Local op2 = createLocal(ir, instruction, instruction.getUse(1), typeInference);

        _writer.writeAssignBinop(m, instruction, l, op1, op2, session);
    }
    private void generate(IMethod m, IR ir, SSAComparisonInstruction instruction, Session session, TypeInference typeInference)
    {
        // Binary instructions have two uses and a single def
        Local l = createLocal(ir, instruction, instruction.getDef(), typeInference);
        Local op1 = createLocal(ir, instruction, instruction.getUse(0), typeInference);
        Local op2 = createLocal(ir, instruction, instruction.getUse(1), typeInference);

        _writer.writeAssignComparison(m, instruction, l, op1, op2, session);
    }

    private void generate(IMethod inMethod, IR ir, SSAThrowInstruction instruction, Session session, TypeInference typeInference)
    {
        // Throw instructions have a single use and no defs
        SymbolTable symbolTable = ir.getSymbolTable();
        int use = instruction.getUse(0);

        if(!symbolTable.isConstant(use))
        {
            Local l = createLocal(ir, instruction, use, typeInference);

            _writer.writeThrow(inMethod, instruction, l, session);
        }
        else if(symbolTable.isNullConstant(use))
        {
            _writer.writeThrowNull(inMethod, instruction, session);
        }
        else
        {
            throw new RuntimeException("Unhandled throw statement: " + instruction);
        }
    }

    private int getNextNonNullInstruction(IR ir, int instructionIndex)
    {
        SSAInstruction[] ssaInstructions = ir.getInstructions();
        //ISSABasicBlock basicBlock = ir.getBasicBlockForInstruction(ssaInstructions[instructionIndex]);
        for(int i = instructionIndex +1 ; i < ssaInstructions.length; i++)
        {
            if(ssaInstructions[i]!=null)
                return i;
        }
        return -1;
    }
}