function validate_required(field,alerttxt)
{
with (field)
  {
  if (value==null||value=="")
    {alert(alerttxt);return false}
  else {return true}
  }
}

function validate_format(field,alerttxt)
{
with (field)
  {
    var macReg=/^[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}$/i;
    if (macReg.test(value))
      {return true}
    else
      {alert(alerttxt);return false}
  }
}

function validate_form(thisform)
{
with (thisform)
  {
  if (validate_required(mac,"mac address must be filled out!")==false)
    {mac.focus();return false}
   
  /*if (validate_format(mac,"bad mac address format!")==false)
    {mac.focus();return false}*/
  }
}

