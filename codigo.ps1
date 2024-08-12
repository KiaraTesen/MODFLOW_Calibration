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

ConvertTo-SecureString -AsPlainText -Force -String ('gXOhzrLp2f)FMPbLo-.7R9j0dRC&xk6?')

## NUEVAS ORDENES
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