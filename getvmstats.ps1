#Connect-VIServer -Server $vCenter

Function Main()
{
Param(
[Parameter(Mandatory=$True,Position=0)][string]$scriptfile,[string]$global:GuestUser,[string]$global:GuestPassword
)
$filepath = [System.IO.Path]::GetDirectoryName($scriptfile)
$filename_temp = [System.IO.Path]::GetFileNameWithoutExtension($scriptfile)

CheckCredentials ($global:GuestUser,$global:GuestPassword)

$VMs = Get-VM | where {$_.PowerState -eq "PoweredOn"} | Get-View | where {$_.Guest.GuestFamily -eq "linuxGuest" } | Sort-Object -Property Name
foreach ($VM in $VMs)
{
$vmname = $VM.Name
switch -wildcard ($vmname)
    {
    "*lin*" {
               Get-Item $scriptfile | Copy-VMGuestFile -Destination "/root/" -VM $vmname -LocalToGuest -GuestUser $global:GuestUser -GuestPassword $global:GuestPassword
               $getinfo = "dos2unix /root/get-info.sh >/dev/null 2>&1; sh /root/get-info.sh; rm -rf /root/get-info.sh"
               $output = Invoke-VMScript -VM $vmname -GuestUser $global:GuestUser -GuestPassword $global:GuestPassword -ScriptType bash -ScriptText $getinfo
               "$vmname`t`t`t$output"
               }
    "*cent*" {
               Get-Item $scriptfile | Copy-VMGuestFile -Destination "/root/" -VM $vmname -LocalToGuest -GuestUser $global:GuestUser -GuestPassword logalpha
               $getinfo = "dos2unix /root/get-info.sh >/dev/null 2>&1; sh /root/get-info.sh; rm -rf /root/get-info.sh"
               $output = Invoke-VMScript -VM $vmname -GuestUser $global:GuestUser -GuestPassword logalpha -ScriptType bash -ScriptText $getinfo
               "$vmname`t`t`t$output"
               }
    "*win*" {
               Get-Item $scriptfile | Copy-VMGuestFile -Destination "/root/" -VM $vmname -LocalToGuest -GuestUser $global:GuestUser -GuestPassword $global:GuestPassword
               $getinfo = "dos2unix /root/get-info.sh >/dev/null 2>&1; sh /root/get-info.sh; rm -rf /root/get-info.sh"
               $output = Invoke-VMScript -VM $vmname -GuestUser $global:GuestUser -GuestPassword $global:GuestPassword -ScriptType bash -ScriptText $getinfo
               "$vmname`t`t`t$output"
               }
    default {
               Get-Item $scriptfile | Copy-VMGuestFile -Destination "/root/" -VM $vmname -LocalToGuest -GuestUser $global:GuestUser -GuestPassword $global:GuestPassword
               $getinfo = "dos2unix /root/get-info.sh >/dev/null 2>&1; sh /root/get-info.sh; rm -rf /root/get-info.sh"
               $output = Invoke-VMScript -VM $vmname -GuestUser $global:GuestUser -GuestPassword $global:GuestPassword -ScriptType bash -ScriptText $getinfo
               "$vmname`t`t`t$output The project that this VM belongs to is unknown"
               }
    }
}
}

Function CheckCredentials()
{
while  (!($global:GuestUser)) {
#Write-Host "Guest username is NULL ... "
$global:GuestUser = Read-Host 'username'
$global:GuestPassword = Read-Host -assecurestring 'password'
}
}

Main