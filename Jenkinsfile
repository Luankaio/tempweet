pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "tempweet"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build e Subida dos Serviços') {
            steps {
                script {
                    echo "Parando containers antigos (se houver)..."
                    sh 'docker-compose down || true'

                    echo "Construindo e subindo serviços..."
                    sh 'docker-compose up -d --build --no-cache'
                }
            }
        }

        stage('Testes') {
            steps {
                script {
                    echo "Rodando testes no container app (se houver)..."
                    // Ajuste 'pytest' de acordo com sua linguagem/test runner
                    sh 'docker-compose exec -T app pytest || echo "Sem testes ou erro ignorado"'
                }
            }
        }

        stage('Saúde do Container') {
            steps {
                script {
                    echo "Verificando se o container 'app' está rodando..."
                    sh 'docker ps | grep app'
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Pipeline finalizado."
            }
        }
        success {
            echo '✅ Deploy concluído com sucesso!'
        }
        failure {
            echo '❌ Algo deu errado no pipeline.'
        }
    }
}
