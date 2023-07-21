param()
#$i = [int]($p1)         # Initial machine

$vm = [int]((hostname) -replace '\D+(\d+)','$1')
#$vms = [int]($p2)       # Last machine
$ip = 10+$vm

Write-Host $vm
cargo run -- --ip "10.0.0.$ip" --port 8888 --service DE --subnet 10.0.0
   
#for(; $i -le $vms; $i++){
 #  
  #   }
