## Ansible SSH Keys
```sh
ssh-agent tcsh
ssh-add ~/Documents/PSK/Keys/spmzt.gate.key.pem
```
ansible-playbook -i inventory.txt amicitia/playbook.yml
