# Ansible AWX Notes

AWX is the open-source, upstream version of Ansible Automation Platform (AAP). These are my notes for installing and using AWX.

-----

## Requirements

One (1) Control Node, real or virtual, with a Linux operating system and the latest version of Mozilla Firefox, with the following minimum resources:

| Purpose                    | Architecture  | CPUs  | Memory  | Storage  | Booting  |
|----------------------------|---------------|:-----:|---------|----------|----------|
| Ansible Control Node       | x86_64        |   4   | 16 GB   | 40 GB    | EFI/UEFI |

> **NOTE** - AWX has the same resource requirements as the Ansible Automation Platform. For more information on AAP requirements, see <https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform/2.2/html/red_hat_ansible_automation_platform_installation_guide/index>.

-----

## Steps

1. Create a directory to hold AWX-related files in your home directory:

    ```bash
    mkdir -p ~/AWX
    cd ~/AWX
    ```

2. Set up minikube:

    ```bash
    cd ~/AWX
    # Get and install the minikube binary
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    ls -la minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    minikube version --short
    # Start minikube with a link to your AWX projects directory
    minikube start --cpus=4 --memory=6g --addons=ingress
    # Update kubectl
    minikube kubectl -- get pods -A
    minikube kubectl version
    # Get information about nodes
    minikube kubectl -- get nodes
    # Change the namespace from 'default' to 'awx'
    kubectl config set-context --current --namespace=awx
    # Enable an alias for the kubectl command line tool
    alias kubectl="minikube kubectl --"
    # Make sure the alias works
    # minikube kubectl -- get pods -A
    kubectl get pods -A
    # Get the IPv4 address of the primary control plane
    minikube ip
    ```

3. Install the latest version of Kustomize:

    ```bash
    curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
    sudo install -o root -g root -m 0755 kustomize /usr/local/bin/kustomize
    ```

4. Get the number of the latest awx-operator release from <https://github.com/ansible/awx-operator/releases>. Then, using an editor of your your choice, create a Kubernetes manifest. Ensure that you replace each instance of `2.10.0` with the latest version:

    > **NOTE** - You do not have to include comments or modelines (indicated by a number sign (`#`)).

    ```yaml
    ---
    # From <https://monokle.io/blog/common-errors-found-in-kubernetes-manifests>:
    # A Kubernetes manifest is a YAML file that describes each component or resource of your
    # deployment and the state you want your cluster to be in once applied.
    # Usage: kustomize build . | kubectl apply -f -
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    resources:
      # Find the latest tag here: https://github.com/ansible/awx-operator/releases
      - github.com/ansible/awx-operator/config/default?ref=2.10.0

    # Set the image tags to match the git version from above
    images:
      - name: quay.io/ansible/awx-operator
        newTag: 2.10.0

    # Specify a custom namespace in which to install AWX
    namespace: awx
    ...
    # code: language=yaml
    # vi: set noai nu ts=2 sw=2 sts=2 sta et:
    ```

5. Apply the manifest:

    ```bash
    kustomize build . | kubectl delete -f -
    kustomize build . | kubectl apply -f -
    ```

6. Wait a minute, then check if the awx-operator is running:

    ```bash
    sleep 60
    # minikube kubectl -- get pods --namespace awx
    kubectl get pods -n awx
    ```

7. Using an editor of your your choice, create a manifest for a demo instance named `awx-demo.yml` with the following contents:

    ```yaml
    ---
    # Manifest for a demo instance
    # kubectl apply -f awx-demo.yml
    apiVersion: awx.ansible.com/v1beta1
    kind: AWX
    metadata:
      name: awx-demo
    spec:
      service_type: nodeport
    ...
    # code: language=yaml
    # vi: set noai nu ts=2 sw=2 sts=2 sta et:
    ```

8. Apply the AWX instance in your cluster:

    ```bash
    kubectl apply -f awx-demo.yml
    ```

9. Wait a minute, then check if the instance is running:

    ```bash
    sleep 60
    # minikube kubectl -- get pods --namespace awx
    kubectl get pods -n awx
    ```

    > **NOTE** - Do not continue to the next step until the `awx-demo-task` and `awx-demo-web` pods are running. If the pods have not started after 5 minutes, use the `minikube logs | tail` and `kubectl get events` commands to check for and troubleshoot any issues,

10. Get the initial password for the AWX **admin** user:

    ```bash
    # minikube kubectl -- get secret awx-demo-admin-password -o jsonpath="{.data.password}" --namespace awx | base64 --decode ; echo
    kubectl get secret awx-demo-admin-password -o jsonpath="{.data.password}" -n awx | base64 --decode ; echo
    ```

11. Get the AWX URL and port number:

    ```bash
    minikube service -n awx awx-demo-service --url
    ```

12. Access AWX through a web browser:

    ```bash
    firefox <the awx-demo-service URL and port>
    ```

    The username is **admin** and the password is the admin secret you retrieved earlier. Once the browser opens, I suggest you change your password.

13. Since the URL changes each time the system restarts, run these commands to reopen AWX:

    ```bash
    minikube stop
    minikube start
    minikube service -n awx awx-demo-service --url
    firefox <the awx-demo-service URL and port; e.g., http://192.168.59.100:31585>
    ```

-----

## Remove AWX and Minikube

If you have to reset your system, run the following commands:

```bash
kubectl delete awx awx-demo
# Delete all profiles and the '.minikube' folder from the home directory
minikube delete --all --purge
minikube stop
unalias kubectl
sudo rm -r /usr/local/bin/minikube
sudo rm -r /usr/local/bin/kustomize
sudo rm -r ~/.kube
sudo rm -r ~/.minikube
```

You may also remove the AWX directory, if you are not reinstalling AWX.

-----

## References

- <https://github.com/ansible/awx>
- <https://github.com/ansible/awx/blob/devel/INSTALL.md>
- <https://github.com/ansible/awx-operator>
- <https://minikube.sigs.k8s.io/docs/start/>
- <https://kubectl.docs.kubernetes.io/installation/kustomize/binaries/>
- <https://minikube.sigs.k8s.io/docs/handbook/persistent_volumes/>
