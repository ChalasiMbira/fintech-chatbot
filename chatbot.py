#!/usr/bin/env python3
"""
Fintech Chatbot Application

A professional chatbot for financial services that handles common customer inquiries
including account information, transactions, and general financial guidance.

Author: Junior Developer
Date: 2025
"""

import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


# Configure logging for production readiness
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IntentType(Enum):
    """Enumeration of supported chatbot intents"""
    GREETING = "greeting"
    ACCOUNT_BALANCE = "account_balance"
    TRANSACTION_HISTORY = "transaction_history"
    TRANSFER_MONEY = "transfer_money"
    LOAN_INFO = "loan_info"
    INVESTMENT_ADVICE = "investment_advice"
    SUPPORT = "support"
    GOODBYE = "goodbye"
    UNKNOWN = "unknown"


@dataclass
class UserSession:
    """Data class to manage user session state"""
    user_id: str
    authenticated: bool = False
    context: Dict = None
    last_intent: Optional[IntentType] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}


class SecurityValidator:
    """Handles security validation and input sanitization"""
    
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """
        Sanitize user input to prevent injection attacks
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Sanitized input string
        """
        if not isinstance(user_input, str):
            return ""
        
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>"\';]', '', user_input)
        return sanitized.strip()
    
    @staticmethod
    def validate_account_number(account_number: str) -> bool:
        """
        Validate account number format
        
        Args:
            account_number: Account number to validate
            
        Returns:
            True if valid format, False otherwise
        """
        # Simple validation - in production, use more robust validation
        pattern = r'^\d{10,12}$'
        return bool(re.match(pattern, account_number))
    
    @staticmethod
    def validate_amount(amount: str) -> Tuple[bool, float]:
        """
        Validate monetary amount
        
        Args:
            amount: Amount string to validate
            
        Returns:
            Tuple of (is_valid, parsed_amount)
        """
        try:
            parsed_amount = float(amount.replace('$', '').replace(',', ''))
            return parsed_amount > 0, parsed_amount
        except (ValueError, AttributeError):
            return False, 0.0


class IntentClassifier:
    """Natural Language Processing for intent classification"""
    
    def __init__(self):
        """Initialize the intent classifier with keyword mappings"""
        self.intent_keywords = {
            IntentType.GREETING: ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            IntentType.ACCOUNT_BALANCE: ['balance', 'account balance', 'how much', 'funds'],
            IntentType.TRANSACTION_HISTORY: ['transactions', 'history', 'statement', 'activity'],
            IntentType.TRANSFER_MONEY: ['transfer', 'send money', 'pay', 'wire'],
            IntentType.LOAN_INFO: ['loan', 'mortgage', 'credit', 'borrow'],
            IntentType.INVESTMENT_ADVICE: ['invest', 'portfolio', 'stocks', 'bonds', 'mutual funds'],
            IntentType.SUPPORT: ['help', 'support', 'customer service', 'problem'],
            IntentType.GOODBYE: ['bye', 'goodbye', 'exit', 'quit', 'thank you']
        }
    
    def classify_intent(self, user_input: str) -> IntentType:
        """
        Classify user intent based on input text
        
        Args:
            user_input: User's message
            
        Returns:
            Classified intent type
        """
        user_input_lower = user_input.lower()
        
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                logger.info(f"Intent classified: {intent.value}")
                return intent
        
        logger.info("Intent classified: unknown")
        return IntentType.UNKNOWN


class ResponseGenerator:
    """Generates contextual responses based on user intent"""
    
    def __init__(self):
        """Initialize response templates"""
        self.responses = {
            IntentType.GREETING: [
                "Hello! Welcome to SecureBank. How can I assist you today?",
                "Hi there! I'm here to help with your banking needs. What can I do for you?",
                "Good day! How may I help you with your financial services today?"
            ],
            IntentType.GOODBYE: [
                "Thank you for using SecureBank! Have a great day!",
                "Goodbye! Feel free to reach out anytime you need assistance.",
                "Take care! Remember, I'm here 24/7 for your banking needs."
            ]
        }
    
    def generate_response(self, intent: IntentType, session: UserSession, 
                         extracted_data: Dict = None) -> str:
        """
        Generate appropriate response based on intent and context
        
        Args:
            intent: Classified user intent
            session: Current user session
            extracted_data: Any extracted entities from user input
            
        Returns:
            Generated response string
        """
        if extracted_data is None:
            extracted_data = {}
        
        # Handle authentication-required intents
        if intent in [IntentType.ACCOUNT_BALANCE, IntentType.TRANSACTION_HISTORY, 
                     IntentType.TRANSFER_MONEY] and not session.authenticated:
            return self._request_authentication()
        
        # Generate intent-specific responses
        response_map = {
            IntentType.GREETING: lambda: self._get_random_response(IntentType.GREETING),
            IntentType.ACCOUNT_BALANCE: lambda: self._handle_balance_inquiry(session),
            IntentType.TRANSACTION_HISTORY: lambda: self._handle_transaction_history(session),
            IntentType.TRANSFER_MONEY: lambda: self._handle_transfer_request(extracted_data),
            IntentType.LOAN_INFO: lambda: self._handle_loan_inquiry(),
            IntentType.INVESTMENT_ADVICE: lambda: self._handle_investment_inquiry(),
            IntentType.SUPPORT: lambda: self._handle_support_request(),
            IntentType.GOODBYE: lambda: self._get_random_response(IntentType.GOODBYE),
            IntentType.UNKNOWN: lambda: self._handle_unknown_intent()
        }
        
        handler = response_map.get(intent, lambda: self._handle_unknown_intent())
        return handler()
    
    def _get_random_response(self, intent: IntentType) -> str:
        """Get a random response for the given intent"""
        import random
        return random.choice(self.responses[intent])
    
    def _request_authentication(self) -> str:
        """Request user authentication"""
        return ("For security purposes, I'll need to verify your identity first. "
                "Please provide your account number or contact customer service at 1-800-SECURE.")
    
    def _handle_balance_inquiry(self, session: UserSession) -> str:
        """Handle account balance requests"""
        # In production, integrate with actual banking API
        mock_balance = "$2,547.83"
        return f"Your current account balance is {mock_balance}. Is there anything else I can help you with?"
    
    def _handle_transaction_history(self, session: UserSession) -> str:
        """Handle transaction history requests"""
        return ("Here are your recent transactions:\n"
                "• Dec 15: Grocery Store - $85.42\n"
                "• Dec 14: Online Transfer - $200.00\n"
                "• Dec 13: ATM Withdrawal - $60.00\n"
                "Would you like more details about any specific transaction?")
    
    def _handle_transfer_request(self, extracted_data: Dict) -> str:
        """Handle money transfer requests"""
        return ("I can help you with transfers. For security, please visit our secure "
                "online portal or mobile app to complete transfers. You can also call "
                "our customer service at 1-800-SECURE.")
    
    def _handle_loan_inquiry(self) -> str:
        """Handle loan information requests"""
        return ("We offer various loan products including:\n"
                "• Personal loans (5.99% - 15.99% APR)\n"
                "• Auto loans (3.49% - 7.99% APR)\n"
                "• Home mortgages (competitive rates)\n"
                "Would you like to speak with a loan specialist?")
    
    def _handle_investment_inquiry(self) -> str:
        """Handle investment advice requests"""
        return ("Investment advice should be personalized to your financial situation. "
                "I recommend speaking with one of our certified financial advisors. "
                "Would you like me to schedule a consultation for you?")
    
    def _handle_support_request(self) -> str:
        """Handle customer support requests"""
        return ("I'm here to help! For complex issues, you can:\n"
                "• Call customer service: 1-800-SECURE\n"
                "• Visit our website: www.securebank.com/support\n"
                "• Chat with a specialist (Mon-Fri 8AM-8PM)\n"
                "What specific issue can I help you with?")
    
    def _handle_unknown_intent(self) -> str:
        """Handle unrecognized user intents"""
        return ("I'm not sure I understand. I can help you with:\n"
                "• Account balances and transactions\n"
                "• Loan information\n"
                "• General banking questions\n"
                "• Connecting you with customer support\n"
                "How can I assist you today?")


class FintechChatbot:
    """Main chatbot class orchestrating all components"""
    
    def __init__(self):
        """Initialize chatbot with all required components"""
        self.intent_classifier = IntentClassifier()
        self.response_generator = ResponseGenerator()
        self.security_validator = SecurityValidator()
        self.active_sessions: Dict[str, UserSession] = {}
        
        logger.info("Fintech Chatbot initialized successfully")
    
    def create_session(self, user_id: str) -> UserSession:
        """
        Create a new user session
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            New UserSession object
        """
        session = UserSession(user_id=user_id)
        self.active_sessions[user_id] = session
        logger.info(f"New session created for user: {user_id}")
        return session
    
    def get_session(self, user_id: str) -> UserSession:
        """
        Retrieve existing session or create new one
        
        Args:
            user_id: User identifier
            
        Returns:
            UserSession object
        """
        return self.active_sessions.get(user_id) or self.create_session(user_id)
    
    def process_message(self, user_id: str, message: str) -> str:
        """
        Process user message and generate response
        
        Args:
            user_id: User identifier
            message: User's input message
            
        Returns:
            Generated response string
        """
        try:
            # Get or create user session
            session = self.get_session(user_id)
            
            # Sanitize input for security
            sanitized_message = self.security_validator.sanitize_input(message)
            
            if not sanitized_message:
                return "I didn't receive a valid message. Please try again."
            
            # Classify user intent
            intent = self.intent_classifier.classify_intent(sanitized_message)
            session.last_intent = intent
            
            # Extract any relevant data (simplified for demo)
            extracted_data = self._extract_entities(sanitized_message)
            
            # Generate and return response
            response = self.response_generator.generate_response(
                intent, session, extracted_data
            )
            
            logger.info(f"Processed message for user {user_id}: {intent.value}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return ("I apologize, but I encountered an error. Please try again or "
                   "contact customer support at 1-800-SECURE if the issue persists.")
    
    def _extract_entities(self, message: str) -> Dict:
        """
        Extract entities from user message (simplified implementation)
        
        Args:
            message: User message
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {}
        
        # Extract monetary amounts
        amount_pattern = r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        amounts = re.findall(amount_pattern, message)
        if amounts:
            entities['amount'] = amounts[0]
        
        # Extract account numbers (simplified)
        account_pattern = r'\b\d{10,12}\b'
        accounts = re.findall(account_pattern, message)
        if accounts:
            entities['account_number'] = accounts[0]
        
        return entities
    
    def end_session(self, user_id: str) -> None:
        """
        End user session and cleanup resources
        
        Args:
            user_id: User identifier
        """
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
            logger.info(f"Session ended for user: {user_id}")


def main():
    """
    Main function for testing the chatbot
    Demonstrates usage and provides interactive testing capability
    """
    print("=== SecureBank Fintech Chatbot ===")
    print("Type 'quit' to exit\n")
    
    # Initialize chatbot
    bot = FintechChatbot()
    user_id = "test_user_001"
    
    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                response = bot.process_message(user_id, "goodbye")
                print(f"Bot: {response}")
                break
            
            if not user_input:
                continue
            
            # Process message and display response
            response = bot.process_message(user_id, user_input)
            print(f"Bot: {response}\n")
            
    except KeyboardInterrupt:
        print("\n\nGoodbye! Thanks for testing the SecureBank Chatbot.")
    finally:
        # Cleanup
        bot.end_session(user_id)


if __name__ == "__main__":
    main()