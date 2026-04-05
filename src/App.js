import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(
        'https://bxip1rz4rh.execute-api.us-east-2.amazonaws.com/medassist-api',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: question })
        }
      );
      const data = await response.json();
      console.log('API response:', data);
      setResult(data);
    } catch (err) {
      setError('Something went wrong. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header>
        <h1>MedAssist</h1>
        <p>Describe your symptoms and get OTC product suggestions</p>
      </header>

      <form onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Describe your health concern... (e.g., I have a sore throat and mild fever)"
          rows={4}
        />
        <button ty
