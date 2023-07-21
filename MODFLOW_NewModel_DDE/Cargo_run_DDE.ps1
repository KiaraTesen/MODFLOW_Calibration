param()
#$i = [int]($p1)         # Initial machine

$vm = [int]((hostname) -replace '\D+(\d+)','$1')
#$vms = [int]($p2)       # Last machine

Write-Host $vm
cargo run -- --ip 10.0.0.(10+$vm) --port 8888 --service DE --subnet 10.0.0
   
#for(; $i -le $vms; $i++){
 #  
  #   }
