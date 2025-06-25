import * as THREE from 'three';

export class PipeManager {
  constructor(scene) {
    this.scene = scene;
    this.pipes = [];
    this.pipeSpeed = 4;
    this.pipeSpacing = 6;
    this.gapSize = 2.5;
    this.nextPipeX = 10;
    this.lastScoredPipe = null;
    
    this.createInitialPipes();
  }
  
  createPipe(x, gapY) {
    const pipeGroup = new THREE.Group();
    
    // Pipe dimensions
    const pipeRadius = 0.5;
    const pipeHeight = 8;
    const capHeight = 0.3;
    const capRadius = 0.7;
    
    // Create upper pipe
    const upperPipeGeometry = new THREE.CylinderGeometry(pipeRadius, pipeRadius, pipeHeight, 16);
    const pipeMaterial = new THREE.MeshLambertMaterial({ color: 0x4CAF50 });
    const upperPipe = new THREE.Mesh(upperPipeGeometry, pipeMaterial);
    upperPipe.position.y = gapY + this.gapSize / 2 + pipeHeight / 2;
    upperPipe.castShadow = true;
    upperPipe.receiveShadow = true;
    pipeGroup.add(upperPipe);
    
    // Upper pipe cap
    const upperCapGeometry = new THREE.CylinderGeometry(capRadius, capRadius, capHeight, 16);
    const capMaterial = new THREE.MeshLambertMaterial({ color: 0xFF8C00 });
    const upperCap = new THREE.Mesh(upperCapGeometry, capMaterial);
    upperCap.position.y = gapY + this.gapSize / 2 + capHeight / 2;
    upperCap.castShadow = true;
    pipeGroup.add(upperCap);
    
    // Create lower pipe
    const lowerPipe = new THREE.Mesh(upperPipeGeometry, pipeMaterial);
    lowerPipe.position.y = gapY - this.gapSize / 2 - pipeHeight / 2;
    lowerPipe.castShadow = true;
    lowerPipe.receiveShadow = true;
    pipeGroup.add(lowerPipe);
    
    // Lower pipe cap
    const lowerCap = new THREE.Mesh(upperCapGeometry, capMaterial);
    lowerCap.position.y = gapY - this.gapSize / 2 - capHeight / 2;
    lowerCap.castShadow = true;
    pipeGroup.add(lowerCap);
    
    // Position the entire pipe group
    pipeGroup.position.x = x;
    
    // Add collision boxes for easier collision detection
    const upperBox = new THREE.Box3().setFromObject(upperPipe);
    const lowerBox = new THREE.Box3().setFromObject(lowerPipe);
    
    const pipeData = {
      group: pipeGroup,
      upperBox: upperBox,
      lowerBox: lowerBox,
      x: x,
      gapY: gapY,
      scored: false
    };
    
    this.pipes.push(pipeData);
    this.scene.add(pipeGroup);
    
    return pipeData;
  }
  
  createInitialPipes() {
    // Create several pipes ahead of the bird
    for (let i = 0; i < 4; i++) {
      const x = this.nextPipeX + i * this.pipeSpacing;
      const gapY = (Math.random() - 0.5) * 3; // Random gap height
      this.createPipe(x, gapY);
    }
    this.nextPipeX += 4 * this.pipeSpacing;
  }
  
  update(deltaTime, gameSpeed) {
    const effectiveSpeed = this.pipeSpeed * gameSpeed;
    
    // Move all pipes
    for (let i = this.pipes.length - 1; i >= 0; i--) {
      const pipe = this.pipes[i];
      pipe.group.position.x -= effectiveSpeed * deltaTime;
      pipe.x = pipe.group.position.x;
      
      // Update collision boxes
      pipe.upperBox.setFromObject(pipe.group.children[0]);
      pipe.lowerBox.setFromObject(pipe.group.children[2]);
      
      // Remove pipes that are far behind
      if (pipe.x < -15) {
        this.scene.remove(pipe.group);
        this.pipes.splice(i, 1);
      }
    }
    
    // Add new pipes when needed
    if (this.pipes.length > 0 && this.pipes[this.pipes.length - 1].x < 20) {
      const gapY = (Math.random() - 0.5) * 3;
      this.createPipe(this.nextPipeX, gapY);
      this.nextPipeX += this.pipeSpacing;
    }
  }
  
  checkCollision(birdPosition) {
    const birdBox = new THREE.Box3().setFromCenterAndSize(
      birdPosition, 
      new THREE.Vector3(0.8, 0.8, 0.8)
    );
    
    for (const pipe of this.pipes) {
      if (Math.abs(pipe.x - birdPosition.x) < 2) {
        if (birdBox.intersectsBox(pipe.upperBox) || birdBox.intersectsBox(pipe.lowerBox)) {
          return true;
        }
      }
    }
    
    return false;
  }
  
  checkScoring(birdX) {
    let points = 0;
    
    for (const pipe of this.pipes) {
      if (!pipe.scored && birdX > pipe.x + 0.5) {
        pipe.scored = true;
        points += 1;
      }
    }
    
    return points;
  }
  
  reset() {
    // Remove all pipes
    for (const pipe of this.pipes) {
      this.scene.remove(pipe.group);
    }
    this.pipes = [];
    this.nextPipeX = 10;
    this.lastScoredPipe = null;
    
    // Create new initial pipes
    this.createInitialPipes();
  }
}