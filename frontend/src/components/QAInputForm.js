import React, { useState } from 'react';
import axios from 'axios';

const QAInputForm = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [responseMessage, setResponseMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!question || !answer) {
            setResponseMessage("Please provide both a question and an answer.");
            return;
        }

        try {
            const response = await axios.post('http://localhost:5000/upload-qa', { question, answer });
            setResponseMessage(response.data.message || "Q&A ingested successfully.");
        } catch (error) {
            setResponseMessage("Error: " + (error.response?.data?.error || error.message));
        }
    };

    return (
        <div>
            <h2>Submit Q&A</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Enter your question"
                />
                <br />
                <textarea
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    placeholder="Enter the answer"
                    rows="5"
                    cols="40"
                ></textarea>
                <br />
                <button type="submit">Submit</button>
            </form>
            <p>{responseMessage}</p>
        </div>
    );
};

export default QAInputForm;
