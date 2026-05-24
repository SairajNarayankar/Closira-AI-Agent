"""
Main entry point for the Closira AI Customer Support Workflow.
Provides a CLI interface for testing the conversation system.
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from conversation_manager import ConversationManager

# Load environment variables
load_dotenv()

console = Console()


def print_welcome():
    """Print welcome message."""
    welcome_text = """
[bold cyan]Closira AI Customer Support Workflow[/bold cyan]
[dim]Bloom Aesthetics Clinic Demo[/dim]

This is a demonstration of an AI-powered customer support system
that handles FAQ, lead qualification, escalation, and summarization.

[yellow]Commands:[/yellow]
- Type your message to chat with the AI
- Type 'quit' or 'exit' to end the conversation
- Type 'state' to see current conversation state
- Type 'help' for more information
    """
    console.print(Panel(welcome_text, border_style="cyan"))


def print_help():
    """Print help information."""
    help_text = """
[bold]How the AI Works:[/bold]

[cyan]Stage 1: FAQ Answering[/cyan]
- Answers questions using only SOP data
- Never makes up information
- Escalates if uncertain

[cyan]Stage 2: Lead Qualification[/cyan]
- Asks structured questions to qualify leads
- Collects customer information
- Stores responses for follow-up

[cyan]Stage 3: Escalation Detection[/cyan]
- Detects negative sentiment
- Identifies out-of-scope questions
- Recognizes explicit escalation requests
- Monitors confidence levels

[cyan]Stage 4: Conversation Summary[/cyan]
- Generates structured summary at end
- Identifies customer intent
- Lists SOP gaps
- Recommends next actions

[yellow]Try asking:[/yellow]
- "What are your Botox prices?"
- "Do you do laser hair removal?" (out of scope)
- "I'm frustrated with this!" (escalation trigger)
- "I'm interested in booking a consultation"
    """
    console.print(Panel(help_text, border_style="yellow"))


def print_response(response: dict):
    """Print AI response with formatting."""
    message = response.get("response", "No response")
    stage = response.get("stage", "unknown")
    confidence = response.get("confidence", 0.0)
    escalated = response.get("escalation_needed", False)
    
    # Color based on stage
    stage_colors = {
        "faq": "green",
        "qualification": "blue",
        "escalation": "red",
        "summary": "magenta"
    }
    color = stage_colors.get(stage, "white")
    
    # Build status line
    status_parts = [f"Stage: {stage.upper()}"]
    if confidence > 0:
        status_parts.append(f"Confidence: {confidence:.2f}")
    if escalated:
        status_parts.append("[red]⚠ ESCALATED[/red]")
    
    status = " | ".join(status_parts)
    
    console.print(f"\n[dim]{status}[/dim]")
    console.print(Panel(message, border_style=color, title="[bold]AI Assistant[/bold]"))


def main():
    """Main function."""
    # Check for Groq API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[red]Error: GROQ_API_KEY not found in environment variables.[/red]")
        console.print("[yellow]Please create a .env file with your FREE Groq API key:[/yellow]")
        console.print("GROQ_API_KEY=your-groq-key-here")
        console.print("\n[cyan]Get your FREE Groq API key at: https://console.groq.com/[/cyan]")
        return
    
    # Initialize conversation manager
    sop_path = Path(__file__).parent / "data" / "sop_data.json"
    
    try:
        manager = ConversationManager(str(sop_path), api_key)
    except FileNotFoundError:
        console.print(f"[red]Error: SOP data file not found at {sop_path}[/red]")
        return
    except Exception as e:
        console.print(f"[red]Error initializing conversation manager: {e}[/red]")
        return
    
    # Print welcome
    print_welcome()
    
    # Main conversation loop
    try:
        while True:
            # Get user input
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit']:
                console.print("\n[yellow]Ending conversation and generating summary...[/yellow]")
                manager.end_conversation()
                break
            
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            elif user_input.lower() == 'state':
                state = manager.get_conversation_state()
                console.print(Panel(
                    f"[cyan]Current Stage:[/cyan] {state['current_stage']}\n"
                    f"[cyan]Messages:[/cyan] {state['message_count']}\n"
                    f"[cyan]Escalated:[/cyan] {state['is_escalated']}\n"
                    f"[cyan]Last Confidence:[/cyan] {state['last_confidence']:.2f}",
                    title="[bold]Conversation State[/bold]",
                    border_style="blue"
                ))
                continue
            
            elif not user_input.strip():
                continue
            
            # Process message
            try:
                response = manager.process_message(user_input)
                print_response(response)
                
                # If escalated, offer to end conversation
                if response.get("escalation_needed", False):
                    console.print("\n[yellow]The conversation has been escalated to a human agent.[/yellow]")
                    end_now = Prompt.ask(
                        "Would you like to end the conversation now?",
                        choices=["yes", "no"],
                        default="yes"
                    )
                    if end_now.lower() == "yes":
                        manager.end_conversation()
                        break
            
            except Exception as e:
                console.print(f"[red]Error processing message: {e}[/red]")
                console.print("[yellow]Please try again or type 'quit' to exit.[/yellow]")
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Conversation interrupted. Generating summary...[/yellow]")
        manager.end_conversation()
    
    console.print("\n[green]Thank you for using Closira AI Customer Support![/green]")


if __name__ == "__main__":
    main()


