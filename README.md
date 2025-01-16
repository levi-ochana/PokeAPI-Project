## 📖 **PokeAPI Project**

### 🌟 **Overview**
This project is a web-based application that integrates with an external Pokémon API to fetch data about Pokémon. The app stores this data in a database and serves it through a microservices architecture deployed on AWS using Infrastructure as Code (IaC) tools and Jenkins for CI/CD.

---

### 🛠️ **Features**
- Fetch Pokémon data from an external API.
- Store Pokémon details in a MongoDB database.
- Microservices architecture:
  - **Backend**: Flask application serving API endpoints.
  - **Frontend**: Web interface for viewing Pokémon details.
- Automated deployment pipeline using Jenkins.
- AWS infrastructure managed with Terraform.
- Dockerized services for portability and scalability.

---

### 💧 **Technologies Used**
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML/CSS/JavaScript 
- **Infrastructure**: AWS (EC2, VPC), Terraform
- **CI/CD**: Jenkins
- **Containerization**: Docker
- **Testing**: Unit tests for Python files
- **Other Tools**: Git, GitHub, Webhooks

---

### 🚀 **Deployment Process**
1. **Infrastructure Setup**:
   - Terraform is used to provision AWS resources (EC2 instances, security groups, etc.).
2. **CI/CD Pipeline**:
   - Jenkins pipeline automates:
     - Cloning the repository.
     - Running unit tests.
     - Building Docker images for the Flask app.
     - Pushing the Docker images to Docker Hub.
     - Deploying MongoDB and Flask containers to EC2 instances.
   - Webhooks trigger the pipeline on each commit.
3. **Application Access**:
   - The frontend is accessible via the public IP of the EC2 instance hosting the web server.

---

### 🗺️ **Project Structure**
![System Diagram](assets/PokeAPI(1).png)

---

### 📝 **To-Do**
- [ ] Add more features to the frontend.
- [ ] Improve error handling in the backend.
- [ ] Enhance testing coverage.

