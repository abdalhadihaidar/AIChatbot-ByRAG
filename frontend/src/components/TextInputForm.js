import React, { useState } from 'react';
import axios from 'axios';

const TextInputForm = () => {
    const [text, setText] = useState('');
    const [responseMessage, setResponseMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!text) {
            setResponseMessage("No text provided.");
            return;
        }

        try {
            const response = await axios.post('http://localhost:5000/upload-text', { text });
            setResponseMessage(response.data.message || "Text ingested successfully.");
        } catch (error) {
            setResponseMessage("Error: " + (error.response?.data?.error || error.message));
        }
    };

    return (
        <div>
            <h2>Submit Text</h2>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Enter your text"
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

export default TextInputForm;
