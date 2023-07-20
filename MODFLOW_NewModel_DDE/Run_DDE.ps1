param($p1, $p2, $p3, $p4, $p5, $p6)

$my_ip = ($p1)
$my_port = ($p2)

$iteration = [int]($p3)
$total_iteration = [int]($p4)
$final_iteration = [int]($p5)

$vms = [int]($p6)

while($iteration -ne $total_iteration){
      #Write-Host "Run experiment : "$iteration
      #Get-Date -Format "dddd MM/dd/yyyy HH:mm K"
      python Methodology_DDE_SCL_CCL.py $my_ip $my_port $iteration $total_iteration $final_iteration $vms
      print($iteration)
      if($error.count -eq 0){
          $iteration++
          $error.clear()
      }
      else{
          Write-Host "Fallo ejecucion : "$iteration
      }
      #Write-Host "Experiment "$iteration " finished"
      #Get-Date -Format "dddd MM/dd/yyyy HH:mm K"
}