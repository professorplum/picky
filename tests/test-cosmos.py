#!/usr/bin/env python3
"""
Helper script to test Cosmos DB configuration locally
"""
import os
import sys

def main():
    print("🧪 Cosmos DB Local Testing Helper")
    print("=" * 50)
    
    # Check if emulator is available
    print("📋 Testing Options:")
    print("1. Azure Cosmos DB Emulator (localhost:8081)")
    print("2. Remote Azure Cosmos DB instance")
    print()
    
    choice = input("Choose option (1-2): ").strip()
    
    if choice == "1":
        print("\n🔧 Setting up for Cosmos DB Emulator...")
        print("Make sure the Azure Cosmos DB Emulator is running!")
        print("Download from: https://aka.ms/cosmosdb-emulator")
        print()
        print("Add these to your .env file:")
        print("COSMOS_ENDPOINT=https://localhost:8081")
        print("COSMOS_KEY=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==")
        print("COSMOS_DATABASE=picky-dev")
        
    elif choice == "2":
        print("\n🌐 Setting up for Remote Azure Cosmos DB...")
        print("You'll need:")
        print("1. A Cosmos DB account in Azure")
        print("2. The endpoint URL and primary key")
        print()
        print("Add these to your .env file:")
        print("COSMOS_ENDPOINT=https://your-account.documents.azure.com:443/")
        print("COSMOS_KEY=your-primary-key-here")
        print("COSMOS_DATABASE=picky-dev")
        
    else:
        print("Invalid choice!")
        return
    
    print("\n🚀 After updating .env, restart your app:")
    print("python run.py")
    print("\n📊 Check the configuration at:")
    print("http://localhost:8000/api/health")

if __name__ == "__main__":
    main()
