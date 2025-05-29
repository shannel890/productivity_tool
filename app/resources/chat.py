from flask_restful import Resource, reqparse
from flask_security import auth_required, current_user
from flask import current_app
from app.models import db, ChatMessage
import json

class ChatResource(Resource):
    @auth_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, required=True,
                          help='Message cannot be blank')
        args = parser.parse_args()
        
        try:
            # Save user message
            user_msg = ChatMessage(
                user_id=current_user.id,
                content=args['message'],
                is_bot=False
            )
            db.session.add(user_msg)
            
            # Generate response (placeholder - replace with actual AI logic)
            response_text = self._generate_response(args['message'])
            
            # Save bot response
            bot_msg = ChatMessage(
                user_id=current_user.id,
                content=response_text,
                is_bot=True
            )
            db.session.add(bot_msg)
            db.session.commit()
            
            return {
                'status': 'success',
                'response': response_text
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"Error processing message: {str(e)}")
            db.session.rollback()
            return {
                'status': 'error',
                'message': 'An error occurred while processing your message'
            }, 500
    
    def _generate_response(self, message):
        """
        Generate a contextual response based on the user's message.
        """
        message = message.lower()
        
        # Common greetings
        if any(word in message for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I help you today?"
            
        # Questions about capabilities
        elif any(word in message for word in ['can you', 'what do you do', 'help me']):
            return "I'm an AI assistant that can help you with various tasks. Feel free to ask me questions!"
            
        # Questions about the assistant
        elif any(word in message for word in ['who are you', 'what are you']):
            return "I'm an AI chatbot designed to help you with your questions and tasks."
            
        # Gratitude
        elif any(word in message for word in ['thanks', 'thank you']):
            return "You're welcome! Is there anything else I can help you with?"
            
        # Goodbye
        elif any(word in message for word in ['bye', 'goodbye']):
            return "Goodbye! Feel free to come back if you have more questions."
            
        # Default response
        else:
            return "I understand you're saying something about '{}'. Could you please elaborate or rephrase that?".format(
                message[:50] + '...' if len(message) > 50 else message
            )

    @auth_required()
    def get(self):
        messages = ChatMessage.query.filter_by(user_id=current_user.id)\
            .order_by(ChatMessage.timestamp.desc())\
            .limit(50)\
            .all()
        return {
            "messages": [
                {
                    "content": msg.content,
                    "is_bot": msg.is_bot,
                    "timestamp": msg.timestamp.isoformat()
                } for msg in reversed(messages)
            ]
        }, 200
