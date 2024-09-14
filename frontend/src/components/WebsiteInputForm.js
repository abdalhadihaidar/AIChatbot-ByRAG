import React, { useState } from 'react';
import axios from 'axios';

const WebsiteInputForm = () => {
    const [url, setUrl] = useState('');
    const [responseMessage, setResponseMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!url) {
            setResponseMessage("Please provide a valid URL.");
            return;
        }

        try {
            const response = await axios.post('http://localhost:5000/upload-website', { url });
            setResponseMessage(response.data.message || "Website content ingested successfully.");
        } catch (error) {
            setResponseMessage("Error: " + (error.response?.data?.error || error.message));
        }
    };

    return (
        <div>
            <h2>Submit Website URL</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter the website URL"
                />
                <br />
                <button type="submit">Submit</button>
            </form>
            <p>{responseMessage}</p>
        </div>
    );
};

export default WebsiteInputForm;
