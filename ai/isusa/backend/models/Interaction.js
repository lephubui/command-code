const mongoose = require('mongoose');

const InteractionSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    stage: {
        type: String,
        required: true
    },
    question: {
        type: String,
        required: true
    },
    advice: {
        type: String,
        required: true
    },
    createdAt: {
        type: Date,
        default: Date.now
    }
});

const Interaction = mongoose.model('Interaction', InteractionSchema);

module.exports = Interaction;