# Flask Hello World

Aplicação simples com Flask para testar as métricas com o AppDynamics. [Pela documentação](https://docs.appdynamics.com/appd/23.x/latest/en/application-monitoring/install-app-server-agents/python-agent/install-the-python-agent-in-containers), o uso recomendado para a instalação do Agent em containers é por meio de um container de proxy.

# Uso

## Docker Compose

Por algum motivo, o container de proxy inicia e termina imediatamente, e não envia para o Controller do AppDynamics.

Para tentar rodar, primeiro é preciso setar a variável de ambiente para o Access Key da conta. Para encontrá-la, [seguir as instruções daqui](https://docs.appdynamics.com/appd/23.x/latest/en/application-monitoring/install-app-server-agents/agent-to-controller-connections#id-.AgenttoControllerConnectionsv23.1-findaccount).

Isso pode ser feito tanto por meio de um arquivo .env:

```
APPDYNAMICS_AGENT_ACCOUNT_ACCESS_KEY=<access_key_value>
```

E rodando:

```bash
docker-compose up -d --build
```

Ou também rodando só:

```bash
APPDYNAMICS_AGENT_ACCOUNT_ACCESS_KEY=<access_key_value> docker-compose up -d --build
```

## Kubernetes

[A documentação](https://docs.appdynamics.com/appd/23.x/latest/en/application-monitoring/install-app-server-agents/python-agent/install-the-python-agent-in-containers) menciona melhor o uso de Kubernetes para fazer o deploy da aplicação junto com o proxy, e desse jeito aparentemente funciona. Localmente, foi testado usando o `minikube`.

As variáveis de ambiente principais estão definidas como um ConfigMap no arquivo `k8s/appd-python-configmap.yaml`. Para aplicá-lo:

```bash
kubectl apply -f k8s/appd-python-configmap.yaml
```

Depois disso, é preciso definir o Access Key da conta. Isso é feito em um Secret do Kubernetes. Para isso, só rodar:

```bash
kubectl create secret generic appd-agent-secret --from-literal=access-key=<access-key>
```

Antes de subir o deployment, é preciso fazer o build da imagem:

```bash
docker build -t flask-hello-world .
```

Por fim, só subir o deployment deveria funcionar:

```bash
kubectl apply -f k8s/appd-python-deployment.yaml
```

Para ver se está rodando:

```bash
kubectl get pods
```