## Seteo WinRM
Set-NetConnectionProfile -NetworkCategory Private
Enable-PSRemoting -Force -SkipNetworkProfileCheck
Set-Item -Path WSMan:\localhost\client\TrustedHosts -Value * -Force

## Seteo de región de trabajo
Set-DefaultAWSRegion -Region us-west-2

## Generar Lista de IP's
$InstanceList = (Get-EC2Instance).Instances.Where({ $PSItem.PublicIpAddress })
$InstanceList

## Desactivar Firewalls
Set-NetFirewallProfile -Name private -Enabled false
Set-NetFirewallProfile -Name public -Enabled false
Set-NetFirewallProfile -Name domain -Enabled false

## Sacar credenciales
foreach ($Instance in $InstanceList) {
Add-Member -InputObject $Instance -MemberType ScriptProperty -Name Credential -Value {
	return [pscredential]::new(($this.PublicIpAddress + '\Administrator'), (ConvertTo-SecureString -AsPlainText -Force -String ('oiGJ$Qr?x&w*(tYKFXXjXrJ8wUD9PM(T')))
    }
Add-Member -InputObject $Instance -MemberType ScriptProperty -Name RemoteSession -Value {
	$ThisSession = Get-PSSession -Name $this.InstanceId -ErrorAction Ignore
	if ($ThisSession) { return $ThisSession }
	else { return New-PSSession -ComputerName $this.PublicIpAddress -Credential $this.Credential -Name $this.InstanceId }
    }
}

## Prueba de conexión
Enter-PSSession -ComputerName $InstanceList[0].PublicIpAddress -Credential $InstanceList[0].Credential
Enter-PSSession -ComputerName $InstanceList[1].PublicIpAddress -Credential $InstanceList[1].Credential

## Activar Remote Session
$InstanceList.RemoteSession

## Ordenes
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\; ls}
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Desktop\; cat prueba.py}

## Credenciales - Desencriptando PEM file
foreach ($Instance in $InstanceList) {
	Add-Member -InputObject $Instance -MemberType ScriptProperty -Name Credential -Value {
		return [pscredential]::new(($this.PublicIpAddress + ‘\Administrator’), (ConvertTo-SecureString -AsPlainText -Force -String (Get-EC2PasswordData -InstanceId $this.InstanceId -Decrypt -PemFile “$Home/ec2_test.pem”)))
}
Add-Member -InputObject $Instance -MemberType ScriptProperty -Name RemoteSession -Value {
	$ThisSession = Get-PSSession -Name $this.InstanceId -ErrorAction Ignore
	if ($ThisSession) { return $ThisSession }
	else { return New-PSSession -ComputerName $this.PublicIpAddress -Credential $this.Credential -Name $this.InstanceId }
}
}

## NUEVAS ORDENES - ADPSO
# Verificar hostnames
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {hostname}

# Actualizar repositorios
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\; git pull}
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DPSO; ls}

# Revisar outputs
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DPSO\output; ls}

# Mandar orden
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DPSO; .\sp\Scripts\activate; powershell './Run_DPSO.ps1 0 201 202'} -AsJob

# Borrar outputs
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DPSO\output; rm iter_*}

## NUEVAS ORDENES - ADDE
# Actualizar repositorios
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\tcp_server\; git pull}														#1
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\; git pull}
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DDE; ls}

# Revisar outputs
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DDE\output; ls}				#2

# Activas - escucha / Mandar orden
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\tcp_server; powershell ‘./Cargo_run_DDE.ps1’} -AsJob				#3
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {Get-Process cargo*}																											#3.1

Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DDE; .\sp\Scripts\activate; powershell ‘./Run_DDE.ps1 0 201 202 20’} -AsJob	#4
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DDE; .\sp\Scripts\activate; powershell ‘./Run_DDE.ps1 0 4 5 4’} -AsJob	#4

# Borrar outputs
Invoke-Command -Session $InstanceList.RemoteSession -ScriptBlock {cd C:\Users\Administrator\Documents\MODFLOW_Calibration\MODFLOW_NewModel_DDE\output; rm iter_*}



foreach ($Instance in $InstanceList) {
Add-Member -InputObject $Instance -MemberType ScriptProperty -Name Credential -Value {
	return [pscredential]::new(($this.PublicIpAddress + '\Administrator'), (ConvertTo-SecureString -AsPlainText -Force -String ('Qw9-H=q)ekympZAPh!C3v;*9P5&XTcqY')))
    }
Add-Member -InputObject $Instance -MemberType ScriptProperty -Name RemoteSession -Value {
	$ThisSession = Get-PSSession -Name $this.InstanceId -ErrorAction Ignore
	if ($ThisSession) { return $ThisSession }
	else { return New-PSSession -ComputerName $this.PublicIpAddress -Credential $this.Credential -Name $this.InstanceId }
    }
}



foreach ($Instance in $InstanceList) {
Add-Member -InputObject $Instance -MemberType ScriptProperty -Name Credential -Value {
	return [pscredential]::new(($this.PublicIpAddress + '\Administrator'), (ConvertTo-SecureString -AsPlainText -Force -String ('7cMOzsA!WsLBj=011!UkVIJOFCtMrkzP')))
    }
Add-Member -InputObject $Instance -MemberType ScriptProperty -Name RemoteSession -Value {
	$ThisSession = Get-PSSession -Name $this.InstanceId -ErrorAction Ignore
	if ($ThisSession) { return $ThisSession }
	else { return New-PSSession -ComputerName $this.PublicIpAddress -Credential $this.Credential -Name $this.InstanceId }
    }
}