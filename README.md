Ansible Playbook
----------------
https://github.com/kelseyhightower/kubernetes-the-hard-way

```
Structure - http://docs.ansible.com/ansible/playbooks_best_practices.html

Execute all tasks defined in the 'localhost' and 'bastion' groups
$ ansible-playbook site.yml -i inventory.py

Vault operations
$ ansible-vault edit vault.yml --vault-password-file ../../vault_password.txt 
$ ansible-vault encrypt vault.yml --vault-password-file ../../vault_password.txt 
$ ansible-vault view vault.yml --vault-password-file ../../vault_password.txt 

View/verify template variable are being set to correct values
$ ansible -m debug -a 'var=hostvars[inventory_hostname]' site
```

DNS
---
```
Host Network
    0.0.0.0:5432 -> pdns_db:5432
    0.0.0.0:5353 -> pdns_recursor:5353
    0.0.0.0:53   -> pdns_nameserver:53
    
pdns_nameserver
    Uses pdns_db for postgresql backend
    Uses pdns_recursor when dns cache misses occur

```