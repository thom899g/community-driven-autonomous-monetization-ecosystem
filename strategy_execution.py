import logging
from typing import Dict, Any
from datetime import datetime
from execution_module.trade_executor import TradeExecutor
from validation_module.strategy_validator import StrategyValidationResult

class StrategyExecution:
    """
    Class responsible for executing validated monetization strategies.
    
    Attributes:
        executor: Instance of TradeExecutor to handle actual trades.
        validator: Instance of StrategyValidator to check strategy validity.
        logger: Logger instance for logging execution events and errors.
    """
    
    def __init__(self, executor: TradeExecutor, validator):
        self.executor = executor
        self.validator = validator
        self.logger = logging.getLogger(__name__)
        
    def execute_strategy(self, strategy: Dict[str, Any]) -> bool:
        """
        Executes a given monetization strategy.
        
        Args:
            strategy: Dictionary containing the strategy parameters and rules.
            
        Returns:
            bool: True if execution was successful, False otherwise.
        """
        try:
            # Validate the strategy before execution
            validation_result = self.validator.validate(strategy)
            if not validation_result.is_valid:
                self.logger.error("Strategy validation failed. %s", validation_result.error_message)
                return False
                
            # Prepare execution parameters
            execution_params = self._prepare_execution_params(strategy)
            
            # Execute the trade
            self.executor.execute(execution_params)
            self.logger.info("Executed strategy successfully at %s.", datetime.now())
            return True
            
        except Exception as e:
            self.logger.error("Exception occurred during strategy execution: %s", str(e))
            raise  # Re-raise the exception to be handled by the caller
            
    def _prepare_execution_params(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepares parameters needed for executing a strategy.
        
        Args:
            strategy: Strategy dictionary containing all necessary parameters.
            
        Returns:
            Dict[str, Any]: Prepared execution parameters.
        """
        # Extract necessary parameters from the strategy
        symbol = strategy.get('symbol', None)
        entry_point = strategy.get('entry_point', None)
        exit_point = strategy.get('exit_point', None)
        
        # Validate required parameters
        if not all([symbol, entry_point, exit_point]):
            raise ValueError("Missing required parameters in strategy.")
            
        # Prepare and return execution parameters
        return {
            'symbol': symbol,
            'entry_point': entry_point,
            'exit_point': exit_point,
            'execution_time': datetime.now().isoformat()
        }