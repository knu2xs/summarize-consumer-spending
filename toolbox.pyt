import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "Beast Mode"

        # List of tool classes associated with this toolbox
        self.tools = [CalculateSummary]


class CalculateSummary(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Calculate Summary"
        self.description = ""
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

        # create the input parameter for the input feature layer
        param0 = arcpy.Parameter(
            displayName='Input Feature Layer',
            name='input_table',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )

        def new_field_parameter(displayName, name):
            """
            Helper to quickly create the four field input parameters...DRY baby!
            :param displayName:
            :param name:
            :return:
            """
            # create the parameter object
            param = arcpy.Parameter(
                displayName=displayName,
                name=name,
                datatype='Field',
                parameterType='Required',
                direction='Input',
                enabled=False
            )

            # set the dependency for the feature layer to be populated
            param.parameterDependencies = [param0.name]

            # apply the filter for only numeric data types
            param.filter.list = ['Short', 'Long', 'Float', 'Double']

            # return the parameter object
            return param

        # create the four input field parameters
        param1 = new_field_parameter('Gross Sales Field', 'gross_field')
        param2 = new_field_parameter('Gross Sales - Mean (Average) Field', 'gross_mean_field')
        param3 = new_field_parameter('Average (Per Capita) Sales Field', 'average_field')
        param4 = new_field_parameter('Average (Per Capita) - Mean (Average) Field', 'average_mean_field')

        # create a list of the parameters and return the result
        params = [param0, param1, param2, param3, param4]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # if the input feature layer parameter has been changed and a value is entered
        if parameters[0].altered and parameters[0].value:
            # enable all the field input fields
            parameters[1].enabled = True
            parameters[2].enabled = True
            parameters[3].enabled = True
            parameters[4].enabled = True

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        # ensure fields are not used twice in two input parameters
        message_fields_equal = 'Unique fields must be used for each field parameter. Two of the field input parameters cannot be the same.'

        if (parameters[1].valueAsText == parameters[2].valueAsText or
                    parameters[1].valueAsText == parameters[3].valueAsText or
                    parameters[1].valueAsText == parameters[4].valueAsText):
            parameters[1].setErrorMessage(message_fields_equal)

        if (parameters[2].valueAsText == parameters[1].valueAsText or
                    parameters[2].valueAsText == parameters[3].valueAsText or
                    parameters[2].valueAsText == parameters[4].valueAsText):
            parameters[2].setErrorMessage(message_fields_equal)

        if (parameters[3].valueAsText == parameters[1].valueAsText or
                    parameters[3].valueAsText == parameters[2].valueAsText or
                    parameters[3].valueAsText == parameters[4].valueAsText):
            parameters[3].setErrorMessage(message_fields_equal)

        if (parameters[4].valueAsText == parameters[1].valueAsText or
                    parameters[4].valueAsText == parameters[2].valueAsText or
                    parameters[4].valueAsText == parameters[3].valueAsText):
            parameters[4].setErrorMessage(message_fields_equal)

        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return
