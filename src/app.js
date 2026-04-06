import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const newMessages = [...messages, {role: "user", content: question}];
    setMessages(newMessages);

    try {
      const response = await fetch(
        'https://bxip1rz4rh.execute-api.us-east-2.amazonaws.com/medassist-api',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ messages: newMessages })
        }
      );
      const data = await response.json();
      setResult(data);
      setMessages([...newMessages, {role: "assistant", content: JSON.stringify(data)}]);
    } catch (err) {
      setError('Something went wrong. Please try again.');
    }
    setLoading(false);
    setQuestion('');
  };

  const startNewConsultation = () => {
    setMessages([]);
    setResult(null);
    setQuestion('');
    setError(null);
  };

  return (
    <div className="App">
      <header>
        <h1>Med<span>Assist</span></h1>
        <p>Describe your symptoms. Get instant OTC and supplement recommendations.</p>
      </header>

      <form onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={messages.length === 0
            ? "What's going on? (e.g., I've had a sore throat and mild fever for two days...)"
            : "Answer the follow-up or ask your own question..."
          }
          rows={3}
        />
        <button type="submit" disabled={loading || !question.trim()}>
          {loading ? 'Analyzing...' : messages.length === 0 ? 'Get Recommendations' : 'Send Follow-up'}
        </button>
      </form>

      {loading && (
        <div className="loader">
          <div className="pulse"></div>
          <p>{messages.length === 0 ? 'Analyzing your symptoms...' : 'Updating recommendations...'}</p>
        </div>
      )}

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="results">
          <div className="card condition">
            <h2>{result.condition}</h2>
            <span className={`severity ${result.severity}`}>
              {result.severity === 'see_doctor' ? 'See a Doctor' : result.severity}
            </span>
            <p>{result.explanation}</p>
          </div>

          <div className="card">
            <h3>OTC Products</h3>
            <ul>
              {result.otc_products && result.otc_products.map((product, i) => (
                <li key={i}>
                  <div className="product-header">
                    <div className="product-name">{product.name}</div>
                    <div className="product-price">{product.price}</div>
                  </div>
                  <div className="product-ingredient">{product.active_ingredient}</div>
                  <div className="product-explanation">{product.how_it_helps}</div>
                  {product.url && (
                    <a href={product.url} target="_blank" rel="noopener noreferrer" className="product-link">
                      View on Amazon →
                    </a>
                  )}
                </li>
              ))}
            </ul>
          </div>

          <div className="card">
            <h3>Supplements</h3>
            <ul>
              {result.supplements && result.supplements.map((supp, i) => (
                <li key={i}>
                  <div className="product-header">
                    <div className="product-name">{supp.name}</div>
                    <div className="product-price">{supp.price}</div>
                  </div>
                  <div className="product-ingredient">{supp.active_ingredient}</div>
                  <div className="product-explanation">{supp.how_it_helps}</div>
                  {supp.url && (
                    <a href={supp.url} target="_blank" rel="noopener noreferrer" className="product-link">
                      View on Amazon →
                    </a>
                  )}
                </li>
              ))}
            </ul>
          </div>

          <div className="card warning">
            <h3>When to See a Doctor</h3>
            <p>{result.when_to_see_doctor}</p>
          </div>

          {result.follow_up_question && (
            <div className="card follow-up">
              <h3>Follow-up Question</h3>
              <p>{result.follow_up_question}</p>
            </div>
          )}

          <div className="disclaimer">
            {result.disclaimer}
          </div>

          {messages.length >= 10 && (
            <button className="new-consultation" onClick={startNewConsultation}>
              Start New Consultation
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
