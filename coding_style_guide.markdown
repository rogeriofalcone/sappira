#Coding Style Guide
###Sappira
* * *
Revision: 0.1

Author: Farhan Ahmed

Date: 11.03.2009
* * *

###General Style Guidelines
- Only use tabs. Do not use spaces for indentation.
- Do not use asterisks (*) in the import statement. Always specify which models/forms/etc. are being imported
- Don't add imports if they are not used.
- Unless the code is obvious, always add the descriptor for the method.
- Use descriptive names for variables, methods, etc. Do not abbreviate these names, unless the abbreviation is well known. If you do use abbreviations qualify them in the comments. So nobody needs to guess what it means.
- Format the *render_to_response* like:

    <pre>
    return render_to_response(
        "template_name.html",
        {"dictionary": variable_name},
        context_instance = RequestContext(request, processors=[custom_proc]),
    )
    </pre>
    
    If there are numerous dictionary values and the width if more than 80 chars put them on the multiple lines like this:
    <pre>
    return render_to_response(
        "template_name.html",
        {
            "dictionary": variable_name, "another_one": item_2, 
            "another_item": item_3, "yet_another_item": item_4,
            "and_another_item": item_5, ...
        },
        context_instance = RequestContext(request, processors=[custom_proc]),
    )
    </pre>
    
    Always include the custom processor in the context. This generally include session level info about the user and whatever else that app needs to make available to the template.