"""Chat Integration Helper - Help AI system mention interpretations transparently

Provides utilities for AI responses to include interpretation details and
ask for user confirmation when needed.
"""

from typing import Dict, Any, Optional, List
from llm.input_interpreter import (
    interpret_input,
    InterpretationResult,
    MatchConfidence,
)


class ChatIntegrationHelper:
    """Helper for integrating input interpretation into chat responses"""
    
    @staticmethod
    def build_interpreted_fields_message(
        interpretations: Dict[str, InterpretationResult]
    ) -> str:
        """
        Build a message that mentions all interpreted fields
        
        Args:
            interpretations: Dict of field_type -> InterpretationResult
            
        Returns:
            Markdown formatted message mentioning interpretations
        """
        if not interpretations:
            return ""
        
        message_parts = []
        
        for field_type, result in interpretations.items():
            if result.confidence == MatchConfidence.EXACT:
                # No mention needed for exact matches
                continue
            
            if result.confidence == MatchConfidence.NO_MATCH:
                continue
            
            # Build interpretation message
            mention = f"📝 **{field_type.title()}**: Saya gunakan **{result.interpreted_value}**"
            
            if result.confidence == MatchConfidence.MEDIUM:
                mention += " (cocok sedang)"
            elif result.confidence == MatchConfidence.LOW:
                mention += " (cocok rendah)"
            
            if result.alternatives:
                mention += f"\n   Alternatif: {', '.join(result.alternatives)}"
            
            message_parts.append(mention)
        
        if not message_parts:
            return ""
        
        return "\n\n" + "\n\n".join(message_parts) + "\n\nBenar demikian?"
    
    @staticmethod
    def build_confirmation_request(
        field_type: str,
        result: InterpretationResult,
        action_name: str = ""
    ) -> Dict[str, Any]:
        """
        Build a complete confirmation request for user
        
        Args:
            field_type: Type of field being confirmed
            result: InterpretationResult
            action_name: Name of action being performed
            
        Returns:
            Dict with confirmation message and details
        """
        confirmation_msg = (
            f"🔍 **{field_type.title()} Confirmation**\n\n"
            f"User input: `{result.original_input}`\n"
            f"Interpretasi saya: **{result.interpreted_value}**\n"
        )
        
        if result.confidence == MatchConfidence.MEDIUM:
            confirmation_msg += "Tingkat kecocokan: Sedang ⚠️\n"
        elif result.confidence == MatchConfidence.LOW:
            confirmation_msg += "Tingkat kecocokan: Rendah ⚠️⚠️\n"
        
        confirmation_msg += "\nBenar? Respons dengan 'ya' atau 'tidak'"
        
        return {
            "requires_confirmation": True,
            "confirmation_message": confirmation_msg,
            "field_type": field_type,
            "original_input": result.original_input,
            "interpreted_value": result.interpreted_value,
            "confidence": result.confidence.value,
            "alternatives": result.alternatives or [],
            "action": action_name,
        }
    
    @staticmethod
    def interpret_and_mention_fields(
        fields: Dict[str, str],
        field_types: Dict[str, str],  # field_name -> field_type (account, date, etc)
        **kwargs
    ) -> Dict[str, Any]:
        """
        Interpret multiple fields and return interpretations + mention message
        
        Args:
            fields: Dict of field_name -> user_value
            field_types: Dict of field_name -> field_type_to_interpret
            **kwargs: Additional kwargs for specific field types (e.g., tx_type for category)
            
        Returns:
            Dict with interpretations and mention message
        """
        interpretations = {}
        confirmation_needed = None
        
        for field_name, user_value in fields.items():
            if not user_value:
                continue
            
            field_type = field_types.get(field_name)
            if not field_type:
                continue
            
            # Get specific kwargs for this field
            field_kwargs = {}
            if field_type == "category":
                field_kwargs["tx_type"] = kwargs.get("tx_type", "expense")
            
            # Interpret the field
            result = interpret_input(field_type, user_value, **field_kwargs)
            interpretations[field_name] = result
            
            # If any field needs confirmation, prioritize that
            if result.needs_confirmation and not confirmation_needed:
                confirmation_needed = (field_name, result)
        
        return {
            "interpretations": interpretations,
            "mention_message": ChatIntegrationHelper.build_interpreted_fields_message(
                interpretations
            ),
            "confirmation_needed": confirmation_needed,
        }
    
    @staticmethod
    def format_ai_response_with_interpretations(
        main_response: str,
        interpretations: Dict[str, InterpretationResult],
        include_confirmation: bool = False
    ) -> str:
        """
        Format AI response to include interpretation details
        
        Args:
            main_response: Main AI response text
            interpretations: Dict of interpreted fields
            include_confirmation: Whether to ask for confirmation
            
        Returns:
            Formatted response with interpretation details
        """
        response = main_response
        
        # Add interpretation mentions
        exact_matches = []
        fuzzy_matches = []
        
        for field_name, result in interpretations.items():
            if result.confidence == MatchConfidence.EXACT or result.confidence == MatchConfidence.NO_MATCH:
                continue
            
            mention = (
                f"💭 *{field_name}: '{result.original_input}' -> {result.interpreted_value}* "
                f"({result.confidence.value})"
            )
            
            if result.confidence in [MatchConfidence.MEDIUM, MatchConfidence.LOW]:
                fuzzy_matches.append(mention)
            else:
                exact_matches.append(mention)
        
        if exact_matches or fuzzy_matches:
            response += "\n\n---"
            if fuzzy_matches:
                response += "\n" + "\n".join(fuzzy_matches)
            response += "\n\nBenar demikian? Atau ada yang perlu diubah?"
        
        return response


# Convenience function
def interpret_and_mention(
    fields: Dict[str, str],
    field_types: Dict[str, str],
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience wrapper for ChatIntegrationHelper.interpret_and_mention_fields
    """
    helper = ChatIntegrationHelper()
    return helper.interpret_and_mention_fields(fields, field_types, **kwargs)
