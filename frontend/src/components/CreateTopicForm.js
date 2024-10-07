import React, { useState } from 'react';
import './CreateTopicForm.css';

function CreateTopicForm() {
  const [topicName, setTopicName] = useState('');
  const [partitions, setPartitions] = useState(3);
  const [replicas, setReplicas] = useState(1);
  const [retentionDays, setRetentionDays] = useState(7);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate inputs
    if (partitions < 1 || partitions > 10) {
      alert("Partitions must be between 1 and 10");
      return;
    }
    if (retentionDays < 1 || retentionDays > 30) {
      alert("Retention must be between 1 and 30 days");
      return;
    }

    const response = await fetch('http://localhost:5000/api/create-topic', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        topicName,
        partitions,
        replicas,
        retentionDays,
      }),
    });

    const result = await response.json();
    if (response.ok) {
      alert(result.message);
    } else {
      alert(`Error: ${result.error}`);
    }
  };

  return (
    <div className="form-container">
      <h2>Create Kafka Topic</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Topic Name:</label>
          <input
            type="text"
            value={topicName}
            onChange={(e) => setTopicName(e.target.value)}
            placeholder="Enter topic name"
            required
          />
        </div>
        <div className="form-group">
          <label>Partitions (1-10):</label>
          <input
            type="number"
            value={partitions}
            onChange={(e) => setPartitions(parseInt(e.target.value))}
            min="1"
            max="10"
            required
          />
        </div>
        <div className="form-group">
          <label>Replicas:</label>
          <input
            type="number"
            value={replicas}
            onChange={(e) => setReplicas(parseInt(e.target.value))}
            min="1"
            required
          />
        </div>
        <div className="form-group">
          <label>Retention (Days) (1-30):</label>
          <input
            type="number"
            value={retentionDays}
            onChange={(e) => setRetentionDays(parseInt(e.target.value))}
            min="1"
            max="30"
            required
          />
        </div>
        <div className="button-container">
          <button type="submit">Create Topic</button>
        </div>
      </form>
    </div>
  );
}

export default CreateTopicForm;
