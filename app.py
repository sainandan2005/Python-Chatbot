from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API
genai.configure(api_key='AIzaSyBDz99OMJ5OVaNkYv-g6Us2RCbxKsYpOtA')
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        user_message = request.json['message']
        if not user_message:
            return jsonify({"response": "Please enter a message"}), 400
            
        # Get response from Gemini
        response = model.generate_content(user_message)
        
        # Check if response is valid
        if not response:
            return jsonify({"response": "Sorry, I couldn't generate a response. Please try again."}), 500
            
        # Extract text from response
        response_text = response.text if hasattr(response, 'text') else str(response)
        print(f"Generated response: {response_text}")  # Debug print
        return jsonify({"response": response_text})
    
    except KeyError:
        print("KeyError: 'message' not found in request")
        return jsonify({"response": "Invalid request format"}), 400
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error: {str(e)}")
        print(f"Full error: {error_details}")
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)