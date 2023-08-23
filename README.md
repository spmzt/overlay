## Ansible SSH Keys
```sh
ssh-agent tcsh
ssh-add ~/Documents/Keys/spmzt.key
```
ansible-playbook -i inventory.txt amicitia/playbook.yml
