#!/bin/bash

if ! which minikube &> /dev/null; then
	echo "Minikube is not installed."
	echo "Installing Minikube ..."
	curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
	sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
	exit 1
fi

if ! minikube status | grep -q "Running"; then
	echo "Starting Minikube ..."
	minikube start
else
	echo "Minikube is already running."
fi

echo "Verifying the cluster is running"
kubectl cluster-info

echo "Retrieving available pods"
kubectl get pods --all-namespaces
