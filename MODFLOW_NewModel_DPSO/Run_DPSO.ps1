param($p1, $p2, $p3)

$iteration = [int]($p1)
$total_iteration = [int]($p2)
$final_iteration = [int]($p3)
#$IP = []($p2)
<#
foreach($iteration in 11..$total_iteration){
      Write-Host "Run experiment : "$iteration
      Get-Date -Format "dddd MM/dd/yyyy HH:mm K"
      #python Methodology_DPSO_SCL 10.0.0.11 $iteration
      Write-Host "Experiment "$iteration " finished"
      Get-Date -Format "dddd MM/dd/yyyy HH:mm K"
}
#>

while($iteration -ne $total_iteration){
      #Write-Host "Run experiment : "$iteration
      #Get-Date -Format "dddd MM/dd/yyyy HH:mm K"
      #python Methodology_DPSO_SCL.py 10.0.0.11:8888 $iteration $total_iteration $final_iteration
      #python Methodology_DPSO_SCL_CCL.py 10.0.0.11:8888 $iteration $total_iteration $final_iteration
      python Methodology_DPSO_CCL.py 10.0.0.11:8888 $iteration $total_iteration $final_iteration
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
