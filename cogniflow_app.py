cogniflow_app.py



"""
CogniFlow Enterprise AI Platform
Author: Your Name
Description: Multi-model AI system for enterprise content classification
"""

from transformers import pipeline
import gradio as gr
from datetime import datetime

# Initialize AI Models
print("Loading AI models...")

classifier = pipeline("zero-shot-classification", 
                     model="facebook/bart-large-mnli")

sentiment_analyzer = pipeline("sentiment-analysis", 
                            model="cardiffnlp/twitter-roberta-base-sentiment-latest")

ner_model = pipeline("ner", 
                    model="dslim/bert-base-NER", 
                    aggregation_strategy="simple")

print("Models loaded successfully!")

def analyze_content(text):
    """Complete AI analysis of business content"""
    
    business_categories = [
        "Technical Support", "Customer Billing", "Account Access", 
        "Product Feedback", "Sales Inquiry", "HR/Internal", "Security Issue"
    ]
    priority_levels = ["Critical Emergency", "High Priority", "Standard", "Low Priority"]
    
    # Run all AI models
    category_result = classifier(text, business_categories)
    priority_result = classifier(text, priority_levels)
    sentiment_result = sentiment_analyzer(text)[0]
    entities = ner_model(text)
    
    # Extract high-confidence entities
    important_entities = [entity['word'] for entity in entities if entity['score'] > 0.8]
    keywords = [word for word in text.split() if len(word) > 4][:5]
    
    return {
        "category": category_result['labels'][0],
        "category_confidence": round(category_result['scores'][0], 3),
        "priority": priority_result['labels'][0],
        "priority_confidence": round(priority_result['scores'][0], 3),
        "sentiment": sentiment_result['label'],
        "sentiment_confidence": round(sentiment_result['score'], 3),
        "keywords": keywords,
        "entities": important_entities[:5]
    }

def web_interface(text):
    """Web interface function"""
    
    if not text or not text.strip():
        return "⚠️ Please enter text to analyze!"
    
    try:
        result = analyze_content(text)
        
        output = f"""
╔═══════════════════════════════════════════════╗
║      COGNIFLOW ENTERPRISE AI ANALYSIS         ║
╚═══════════════════════════════════════════════╝

⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 CLASSIFICATION
Category: {result['category']}
Confidence: {result['category_confidence'] * 100:.1f}%

⚡ PRIORITY
Level: {result['priority']}
Confidence: {result['priority_confidence'] * 100:.1f}%

😊 SENTIMENT
Tone: {result['sentiment']}
Confidence: {result['sentiment_confidence'] * 100:.1f}%

🔍 KEY INSIGHTS
Keywords: {', '.join(result['keywords'])}
Entities: {', '.join(result['entities']) if result['entities'] else 'None detected'}
"""
        return output
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Create interface
interface = gr.Interface(
    fn=web_interface,
    inputs=gr.Textbox(lines=5, placeholder="Enter business content..."),
    outputs=gr.Textbox(lines=20),
    title="🚀 CogniFlow Enterprise AI",
    description="Multi-model AI for enterprise content analysis"
)

if __name__ == "__main__":
    interface.launch(share=True)
