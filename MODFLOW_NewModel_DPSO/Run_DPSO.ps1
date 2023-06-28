param($p1, $p2)
#param($p1, $p2)

$total_iteration = [int]($p1)
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
$iteration = [int]($p2)
while($iteration -ne $total_iteration){
      #Write-Host "Run experiment : "$iteration
      #Get-Date -Format "dddd MM/dd/yyyy HH:mm K"
        python Methodology_DPSO_SCL 10.0.0.11 $iteration
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
