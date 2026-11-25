$out = "C:\Users\Lenovo\AppData\Local\Temp\claude\a0f298b805dfcb16\84d6406d-f149-4c45-afef-396d97e96f97\scratchpad"
$files = @(
  @{ doc = "C:\UST\TRANSMA PROJECT\4ECEB_Group5_Report_OPTION_A_Frassati.docx"; pdf = "$out\option_a.pdf" },
  @{ doc = "C:\UST\TRANSMA PROJECT\4ECEB_Group5_Report_OPTION_B_BGPOP.docx"; pdf = "$out\option_b.pdf" }
)
$word = New-Object -ComObject Word.Application
try {
  $word.Visible = $false
  $word.DisplayAlerts = 0
  foreach ($f in $files) {
    $d = $word.Documents.Open($f.doc, $false, $false, $false)
    try {
      foreach ($toc in $d.TablesOfContents) { $toc.Update() }
      foreach ($tof in $d.TablesOfFigures) { $tof.Update() }
      $d.Save()
      $d.ExportAsFixedFormat($f.pdf, 17)
      Write-Output ("{0}: {1} pages" -f (Split-Path $f.doc -Leaf), $d.ComputeStatistics(2))
    } finally {
      $d.Close(0)
    }
  }
} finally {
  $word.Quit(0)
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
}
Get-Process WINWORD -ErrorAction SilentlyContinue | Select-Object Id, StartTime, MainWindowTitle | Format-Table -AutoSize | Out-String | Write-Output
