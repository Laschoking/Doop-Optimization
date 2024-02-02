// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.12;
import {IBuyBack} from "IBuyBack.sol";

contract BuyBackResolver {
    address public immutable buyBackExecutor;

    constructor(address _buyBack) {
        buyBackExecutor = _buyBack;
    }

    function canSellTokens()
        external
        view
        returns (bool canExec, bytes memory execPayload)
    {
        IBuyBack executor = IBuyBack(buyBackExecutor);
        address token = executor.canSellToken();
        if (token != address(0)) {
            canExec = true;
            execPayload = abi.encodeCall(executor.sellTokens, (token));
        }
    }

    function canSendToTreasury()
        external
        view
        returns (bool canExec, bytes memory execPayload)
    {
        IBuyBack executor = IBuyBack(buyBackExecutor);
        if (executor.canSendToTreasury()) {
            canExec = true;
            execPayload = abi.encodeWithSelector(
                executor.sendToTreasury.selector
            );
        }
    }

    function canBurnTokens()
        external
        view
        returns (bool canExec, bytes memory execPayload)
    {
        IBuyBack executor = IBuyBack(buyBackExecutor);
        if (executor.canBurnTokens()) {
            canExec = true;
            execPayload = abi.encodeWithSelector(executor.burnTokens.selector);
        }
    }

    function canTopUpKeeper()
        external
        view
        returns (bool canExec, bytes memory execPayload)
    {
        IBuyBack executor = IBuyBack(buyBackExecutor);
        if (executor.canTopUpKeeper()) {
            canExec = true;
            execPayload = abi.encodeWithSelector(executor.topUpKeeper.selector);
        }
    }
}
