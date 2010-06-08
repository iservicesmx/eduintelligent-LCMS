function evaluation_viewer(portal_url) {
    var url = portal_url;
    var defines = 'dependent=yes,';
    defines += 'toolbar=no,';
    defines += 'location=no,';
    defines += 'status=no,';
    defines += 'menubar=no,';
    defines += 'scrollbars=yes,';
    defines += 'resizable=yes,';
    defines += 'width=700,';
    defines += 'height=500,';
    defines += 'left=300'; 
    
    window.open(url, 'evaluation_view', defines);
}

var countdown_value = 0;

function q_countdown()
{				
    countdown_value--;
    document.forms.testForm.countdown.value = countdown_value;

    if (countdown_value < 1) {
        document.forms.testForm.timeout.value = 1;
        // SendQuestion = document.getElementById("SendQuestion"); 
        document.forms.testForm.btnSubmit.click();
        // SendQuestion.click();
        document.forms.testForm.submit();
    }
    else {
        window.setTimeout("q_countdown()",1000);
    };
}

function q_install_countdown(sec)
{
    countdown_value = sec;
    document.forms.testForm.countdown.value = countdown_value;
    /*field.value = countdown_value;*/
    window.setTimeout("q_countdown()", 1000);
}

function startTimer()
{
   startDate = new Date().getTime();
   document.forms.testForm.timestamp.value = startDate;
   //document.forms.testForm.btnSubmit.disabled=true;
}

function computeTime()
{
   if ( startDate != 0 )
   {
      var currentDate = new Date().getTime();
      var elapsedSeconds = ( (currentDate - startDate) / 1000 );
      var formattedTime = convertTotalSeconds( elapsedSeconds );
   }
   else
   {
      formattedTime = "00:00:00.0";
   }

   document.forms.testForm.latency.value = formattedTime;
}


/*******************************************************************************
** this function will convert seconds into hours, minutes, and seconds in
** CMITimespan type format - HHHH:MM:SS.SS (Hours has a max of 4 digits &
** Min of 2 digits
*******************************************************************************/
function convertTotalSeconds(ts)
{
    var sec = (ts % 60);
    ts -= sec;
    var tmp = (ts % 3600);  //# of seconds in the total # of minutes
    ts -= tmp;              //# of seconds in the total # of hours
    // convert seconds to conform to CMITimespan type (e.g. SS.00)
    sec = Math.round(sec*100)/100;
    var strSec = new String(sec);
    var strWholeSec = strSec;
    var strFractionSec = "";

    if (strSec.indexOf(".") != -1) {
        strWholeSec =  strSec.substring(0, strSec.indexOf("."));
        strFractionSec = strSec.substring(strSec.indexOf(".")+1, strSec.length);
    }

    if (strWholeSec.length < 2) {
       strWholeSec = "0" + strWholeSec;
    }
    strSec = strWholeSec;
    if (strFractionSec.length) {
      strSec = strSec+ "." + strFractionSec;
    }
    if ((ts % 3600) != 0 )
      var hour = 0;
    else var hour = (ts / 3600);
    if ( (tmp % 60) != 0 )
      var min = 0;
    else var min = (tmp / 60);

    if ((new String(hour)).length < 2)
      hour = "0"+hour;
    if ((new String(min)).length < 2)
      min = "0"+min;
    var rtnVal = hour+":"+min+":"+strSec;
 return rtnVal;
}    


/***


**/ 

crir = {
	init: function() {
		arrLabels = document.getElementsByTagName('label');
	
		searchLabels:
		for (var i=0; i<arrLabels.length; i++) {			
			// get the input element based on the for attribute of the label tag
			if (arrLabels[i].getAttributeNode('for') && arrLabels[i].getAttributeNode('for').value != '') {
				labelElementFor = arrLabels[i].getAttributeNode('for').value;				
				inputElement = document.getElementById(labelElementFor);
			}
			else {				
				continue searchLabels;
			}	
							
			inputElementClass = inputElement.className;	
		
			// if the input is specified to be hidden intiate it
			if (inputElementClass == 'crirHiddenJS') {
				inputElement.className = 'crirHidden';
				
				inputElementType = inputElement.getAttributeNode('type').value;	
				
				// add the appropriate event listener to the input element
				if (inputElementType == "checkbox") {
					inputElement.onclick = crir.toggleCheckboxLabel;
				}
				else {
					inputElement.onclick = crir.toggleRadioLabel;
				}
				
				// set the initial label state
				if (inputElement.checked) {
					if (inputElementType == 'checkbox') { arrLabels[i].className = 'checkbox_checked'}
					else { arrLabels[i].className = 'radio_checked' }
				}
				else {
					if (inputElementType == 'checkbox') { arrLabels[i].className = 'checkbox_unchecked'}
					else { arrLabels[i].className = 'radio_unchecked' }
				}
			}
			else if (inputElement.nodeName != 'SELECT' && inputElement.getAttributeNode('type').value == 'radio') { // this so even if a radio is not hidden but belongs to a group of hidden radios it will still work.
				arrLabels[i].onclick = crir.toggleRadioLabel;
				inputElement.onclick = crir.toggleRadioLabel;
			}
		}			
	},	
	
	findLabel: function (inputElementID) {
		arrLabels = document.getElementsByTagName('label');
	
		searchLoop:
		for (var i=0; i<arrLabels.length; i++) {
			if (arrLabels[i].getAttributeNode('for') && arrLabels[i].getAttributeNode('for').value == inputElementID) {				
				return arrLabels[i];
				break searchLoop;				
			}
		}		
	},	
	
	toggleCheckboxLabel: function () {
		labelElement = crir.findLabel(this.getAttributeNode('id').value);
	
		if(labelElement.className == 'checkbox_checked') {
			labelElement.className = "checkbox_unchecked";
		}
		else {
			labelElement.className = "checkbox_checked";
		}
	},	
	
	toggleRadioLabel: function () {			 
		clickedLabelElement = crir.findLabel(this.getAttributeNode('id').value);
		
		clickedInputElement = this;
		clickedInputElementName = clickedInputElement.getAttributeNode('name').value;
		
		arrInputs = document.getElementsByTagName('input');
	
		// uncheck (label class) all radios in the same group
		for (var i=0; i<arrInputs.length; i++) {			
			inputElementType = arrInputs[i].getAttributeNode('type').value;
			if (inputElementType == 'radio') {
				inputElementName = arrInputs[i].getAttributeNode('name').value;
				inputElementClass = arrInputs[i].className;
				// find radio buttons with the same 'name' as the one we've changed and have a class of chkHidden
				// and then set them to unchecked
				if (inputElementName == clickedInputElementName && inputElementClass == 'crirHidden') {				
					inputElementID = arrInputs[i].getAttributeNode('id').value;
					labelElement = crir.findLabel(inputElementID);
					labelElement.className = 'radio_unchecked';
				}
			}
		}
	
		// if the radio clicked is hidden set the label to checked
		if (clickedInputElement.className == 'crirHidden') {
			clickedLabelElement.className = 'radio_checked';
		}
	},
	
	addEvent: function(element, eventType, doFunction, useCapture){
		if (element.addEventListener) 
		{
			element.addEventListener(eventType, doFunction, useCapture);
			return true;
		} else if (element.attachEvent) {
			var r = element.attachEvent('on' + eventType, doFunction);
			return r;
		} else {
			element['on' + eventType] = doFunction;
		}
	}
}

crir.addEvent(window, 'load', crir.init, false);

function finish_question()
{
 computeTime();
 setTimeout('parent.opener.location.reload()',1000);
 //setTimeout('parent.window.close()', 1000);
}

function enableSubmit(myform)
{
    myform.btnSubmit.disabled=false;
   //btn = document.getElementById("btnSubmit");
   //btn.disabled=false;
   
}

counter = 0;
function count() {
    counter++;
    if(counter> 1) {
        if(counter> 2) { return false; }
        alert('Con un solo click es suficiente');
        return false;
    }
return true;
}