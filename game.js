import * as THREE from 'three';
import { SceneManager } from './scene.js';
import { Bird } from './bird.js';
import { PipeManager } from './pipes.js';

export class Game {
  constructor() {
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.clock = new THREE.Clock();
    
    this.gameState = 'playing'; // 'playing', 'gameOver'
    this.score = 0;
    this.gameSpeed = 1.0;
    
    this.setupRenderer();
    this.setupCamera();
    this.initializeGame();
    this.setupEventListeners();
    
    // UI elements
    this.scoreElement = document.getElementById('score');
    this.gameOverElement = document.getElementById('gameOver');
    this.finalScoreElement = document.getElementById('finalScore');
  }
  
  setupRenderer() {
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    document.getElementById('gameContainer').appendChild(this.renderer.domElement);
  }
  
  setupCamera() {
    this.camera.position.set(0, 2, 8);
    this.camera.lookAt(0, 0, 0);
  }
  
  initializeGame() {
    // Initialize scene
    this.sceneManager = new SceneManager(this.scene);
    
    // Initialize bird
    this.bird = new Bird();
    this.scene.add(this.bird.mesh);
    
    // Initialize pipes
    this.pipeManager = new PipeManager(this.scene);
    
    // Camera shake variables
    this.cameraShake = { intensity: 0, duration: 0 };
    this.originalCameraPosition = this.camera.position.clone();
  }
  
  setupEventListeners() {
    // Spacebar and click to flap
    document.addEventListener('keydown', (event) => {
      if (event.code === 'Space') {
        event.preventDefault();
        this.handleFlap();
      }
    });
    
    this.renderer.domElement.addEventListener('click', () => {
      this.handleFlap();
    });
    
    // Touch support
    this.renderer.domElement.addEventListener('touchstart', (e) => {
      e.preventDefault();
      this.handleFlap();
    });
    
    // Window resize
    window.addEventListener('resize', () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });
  }
  
  handleFlap() {
    if (this.gameState === 'playing') {
      this.bird.flap();
    }
  }
  
  updateScore(points) {
    this.score += points;
    this.scoreElement.textContent = this.score;
    
    // Increase game speed slightly with score
    this.gameSpeed = Math.min(2.0, 1.0 + this.score * 0.02);
  }
  
  gameOver() {
    this.gameState = 'gameOver';
    this.finalScoreElement.textContent = this.score;
    this.gameOverElement.style.display = 'block';
    
    // Screen shake effect
    this.cameraShake.intensity = 0.3;
    this.cameraShake.duration = 0.5;
  }
  
  restart() {
    // Reset game state
    this.gameState = 'playing';
    this.score = 0;
    this.gameSpeed = 1.0;
    this.scoreElement.textContent = '0';
    this.gameOverElement.style.display = 'none';
    
    // Reset bird
    this.bird.reset();
    
    // Reset pipes
    this.pipeManager.reset();
    
    // Reset camera
    this.cameraShake.intensity = 0;
    this.cameraShake.duration = 0;
    this.camera.position.copy(this.originalCameraPosition);
  }
  
  updateCameraShake(deltaTime) {
    if (this.cameraShake.duration > 0) {
      this.cameraShake.duration -= deltaTime;
      
      const shakeX = (Math.random() - 0.5) * this.cameraShake.intensity;
      const shakeY = (Math.random() - 0.5) * this.cameraShake.intensity;
      
      this.camera.position.x = this.originalCameraPosition.x + shakeX;
      this.camera.position.y = this.originalCameraPosition.y + shakeY;
      
      if (this.cameraShake.duration <= 0) {
        this.camera.position.copy(this.originalCameraPosition);
      }
    }
  }
  
  update() {
    const deltaTime = this.clock.getDelta();
    
    if (this.gameState === 'playing') {
      // Update bird
      this.bird.update(deltaTime);
      
      // Update pipes
      this.pipeManager.update(deltaTime, this.gameSpeed);
      
      // Check for scoring
      const scoredPoints = this.pipeManager.checkScoring(this.bird.mesh.position.x);
      if (scoredPoints > 0) {
        this.updateScore(scoredPoints);
      }
      
      // Check collisions
      if (this.pipeManager.checkCollision(this.bird.mesh.position) || this.bird.mesh.position.y < -3) {
        this.gameOver();
      }
    }
    
    // Update camera shake
    this.updateCameraShake(deltaTime);
    
    // Update scene animations
    this.sceneManager.update(deltaTime);
  }
  
  render() {
    this.renderer.render(this.scene, this.camera);
  }
  
  start() {
    const animate = () => {
      requestAnimationFrame(animate);
      this.update();
      this.render();
    };
    animate();
  }
}