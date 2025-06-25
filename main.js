import { Game } from './game.js';

// Initialize the game
const game = new Game();
window.game = game; // Make globally accessible for restart button

// Start the game
game.start();