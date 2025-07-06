import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function History({ email }) {
    const [history, setHistory] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await axios.get(`http://localhost:5001/api/history/${email}`);
                console.log(email); // Debugging line to check email
                setHistory(response.data);
            } catch (error) {
                console.error('Error fetching history:', error);
            }
        };

        if (email) {
            fetchHistory();
        }
    }, [email]);

    return (
        <div className="container mt-5">
            <h2>History</h2>
            <button className="btn btn-secondary mt-4" onClick={() => navigate('/')}>Go Back</button>
            <br /><br /> {/* Add a breakline here */}
            {history.length === 0 ? (
                <p>No history available.</p>
            ) : (
                <ul className="list-group">
                    {history.map((item, index) => (
                        <li key={index} className="list-group-item">
                            <h5>Stage: {item.stage}</h5>
                            <p><strong>Question:</strong> {item.question}</p>
                            <p><strong>Advice:</strong> {item.advice}</p>
                            <p><strong>Date:</strong> {new Date(item.createdAt).toLocaleString()}</p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default History;