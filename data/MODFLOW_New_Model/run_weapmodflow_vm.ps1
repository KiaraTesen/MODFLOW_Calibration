param($p1, $p2)

$population_size = [int]($p1)    
$total_number_vm = [int]($p2)

function valores_array($n,$total_mv,$mv){
   $chunk = [int][Math]::Floor($n/$total_mv)

   $rango_inicio = $chunk*($mv-1) + 1

   if(-Not ($mv -eq $total_mv)){
       $rango_final = $rango_inicio + ($chunk-1)
   }else{
       $rango_final = $n
   }
   return $rango_inicio..$rango_final
}

function run_weap(){
  $vm = [int]((hostname) -replace '\D+(\d+)','$1') - 1

  Write-Host "Comenzamos la ejecución en la Máquina Virtual " $vm
  Get-Date -Format "dddd MM/dd/yyyy HH:mm K"

  $ind = valores_array $population_size $total_number_vm $vm
  
  Write-Host "Run experiment : "$ind
  Get-Date -Format "dddd MM/dd/yyyy HH:mm K"
  python run_LP_model.py $ind $population_size
  Write-Host "Experiment "$ind " finished"
  Get-Date -Format "dddd MM/dd/yyyy HH:mm K"
}
run_weap


