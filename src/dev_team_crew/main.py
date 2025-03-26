# src/dev_team_crew/main.py
import os
from dotenv import load_dotenv
from dev_team_crew.crew import DevTeamCrew

# Load environment variables - make sure this runs before any API calls
load_dotenv()

def run():
    """Run the development team crew"""
    
    print("Starting the development team process...")
    print(f"Using Anthropic API key: {os.environ.get('ANTHROPIC_API_KEY', '')[:5]}...")
    
    # Initialize the crew
    dev_crew = DevTeamCrew()
    
    # Create inputs if needed
    inputs = {}
    
    # Launch the crew
    results = dev_crew.crew().kickoff(inputs=inputs)
    
    # Output results
    print("\n=== Development Process Completed ===\n")
    for i, result in enumerate(results):
        print(f"\n--- Result {i+1}: ---\n")
        print(result[:300] + "..." if len(result) > 300 else result)
    
    return results

if __name__ == "__main__":
    run()