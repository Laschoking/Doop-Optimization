package org.clyze.doop.soot;

import java.io.File;
import java.io.IOException;
import java.io.Writer;
import java.util.EnumMap;
import java.util.EnumSet;
import java.util.Map;

class CSVDatabase implements Database
{
    /** The maximum number of characters per column */
    private static final int MAX_COLUMN_LENGTH = 256;

    private static final char SEP = '\t';
    private static final char EOL = '\n';

    private File directory;
    private Map<PredicateFile, Writer> writers;

    CSVDatabase(File directory) throws IOException
    {
        this.directory = directory;
        this.writers = new EnumMap<>(PredicateFile.class);

        for(PredicateFile predicateFile : EnumSet.allOf(PredicateFile.class))
            writers.put(predicateFile, predicateFile.getWriter(directory, ".facts"));
    }

    @Override
    public void close() throws IOException
    {
        for(Writer w: writers.values())
            w.close();
    }

    @Override
    public void flush() throws IOException
    {
        for(Writer w: writers.values())
            w.flush();
    }


    private void addColumn(Writer writer, Column column, boolean shouldTruncate)
        throws IOException
    {
        // Quote some special characters
        String data = column.toString()
            .replaceAll("\"", "\\\\\"")
            .replaceAll("\n", "\\\\n")
            .replaceAll("\t", "\\\\t");

        // Truncate column if necessary
        if (shouldTruncate)
        {
            int length = data.length();

            // TODO: log the event
            if (length > MAX_COLUMN_LENGTH)
                length = MAX_COLUMN_LENGTH;

            writer.write(data, 0, length);
        }
        else {
            writer.write(data);
        }
    }


    @Override
    public void add(PredicateFile predicateFile, Column arg, Column ... args)
    {
        try {
            synchronized(predicateFile) {
                Writer writer = getWriter(predicateFile);
                addColumn(writer, arg, false);
                

                for (Column col : args)
                    addColumn(writer.append(SEP), col, false);

                writer.write(EOL);
            }
        } catch(IOException exc) {
            throw new RuntimeException(exc);
        }
    }


    private Writer getWriter(PredicateFile predicateFile) throws IOException
    {
        return writers.get(predicateFile);
    }


    @Override
    public Column addEntity(PredicateFile predicateFile, String key)
    {
      add(predicateFile, new Column(key));
      return new Column(key);
    }


    @Override
    public Column asColumn(String arg) {
        return new Column(arg);
    }


    @Override
    public Column asEntity(String arg) {
        return new Column(arg);
    }

    @Override
    public Column asEntity(PredicateFile predicateFile, String arg) {
        return new Column(arg);
    }


    @Override
    public Column asIntColumn(String arg) {
        return new Column(arg);
    }
}
