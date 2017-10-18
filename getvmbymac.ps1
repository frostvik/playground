#
#USAGE
#.\getvmbymac.ps1 myvCenter.info Administrator@ddtest.info mypassword 00:50:56:4b:29:33
# one line Get-VM | Where-Object { $_ | get-networkadapter | Where-Object { $_.MacAddress -like '00:50:56:ba:c5:28'} }
#

[CmdletBinding()]
Param(
[Parameter(Mandatory=$True,Position=1)]
[string]$vcServer= $(if ([string]::IsNullOrEmpty($env:vcServer)) {throw "The parameter $vcServer is required .... STOP."}),
[Parameter(Mandatory=$True,Position=2)]
[string]$vcUser= $(if ([string]::IsNullOrEmpty($env:vcUser)) {throw "The parameter $vcUser is required .... STOP."}),
[Parameter(Mandatory=$True,Position=3)]
[string]$vcPass= $(if ([string]::IsNullOrEmpty($env:vcPass)) {throw "The parameter $vcPass is required .... STOP."}),
[Parameter(Mandatory=$True,Position=4)]
[string]$macaddr= $(if ([string]::IsNullOrEmpty($env:targetVm)) {throw "The parameter $macaddr is required .... STOP."})

#Add the core VMware PowerCLI snapin
Add-PSSnapin VMware.VimAutomation.Core

#Connect to the vCenter Server
echo "Connecting to vCenter..."
Connect-VIServer -Server $vcServer -Force -User $vcUser -Password $vcPass | out-null

$report =@()
Get-VM | Get-View | %{
    $VMname = $_.Name 
    $_.guest.net | where {$_.MacAddress -eq "$macaddr"} | %{
        $row = "" | Select VM, MAC
        $row.VM = $VMname
        $row.MAC = $_.MacAddress
        $report += $row
        }
    }
    $report
Disconnect-VIServer * -Confirm:$FALSE