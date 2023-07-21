param($p1, $p2)
$i = [int]($p1)         # Initial machine

$vm = [int]((hostname) -replace '\D+(\d+)','$1')
$vms = [int]($p2)       # Last machine
    
 for(; $i -le $vms; i++){
    Write-Host $i
    #cargo run -- --ip "10.0.0.$($using:i + 10)" --port 8888 --service DE --subnet 10.0.0
 }