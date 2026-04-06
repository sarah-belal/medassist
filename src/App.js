const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Step 1: add user's question to the conversation history
    const newMessages = [...messages, {role: "user", content: question}];
    setMessages(newMessages);

    try {
      const response = await fetch(
        'https://bxip1rz4rh.execute-api.us-east-2.amazonaws.com/medassist-api',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          // Step 2: send full conversation history instead of just the question
          body: JSON.stringify({ messages: newMessages })
        }
      );
      const data = await response.json();
      setResult(data);

      // Step 3: add Claude's response to the conversation history
      setMessages([...newMessages, {role: "assistant", content: JSON.stringify(data)}]);

    } catch (err) {
      setError('Something went wrong. Please try again.');
    }
    setLoading(false);
    setQuestion('');  // clear the input for the next message
  };
