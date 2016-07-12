"""
name:       calculate values by standard deviation
dob:        06 Jul 2016
author:     Joel McCune
"""
# import modules
import math
import arcpy


def get_summary_qualifier_by_standard_deviation(standard_deviation):
    """
    Get the summary value based on the input range the standard deviation value falls into.
    :param summary_root:
    :param standard_deviation:
    :return:
    """
    # round down the standard deviation
    standard_deviation_index = int(math.floor(standard_deviation))

    # dictionary for looking up definitions based on standard deviation breakpoints
    summary_dictionary = {
        3: 'exceptionally strong',
        2: 'very strong',
        1: 'strong',
        0: 'positive',
        -1: 'weak',
        -2: 'very weak',
        -3: 'exceptionally weak'
    }

    # return the correlating value from the lookup
    return summary_dictionary[standard_deviation_index]


def get_gross_summary_by_standard_deviation(value, standard_deviation):
    """
    Get the gross market potential summary based on the input range the standard deviation falls into.
    :param value:
    :param standard_deviation:
    :return: The summary explanation describing what the value means.
    """
    # create the statement
    return 'The potential for gross, or total sales is {0:,0f} dollars, {1:,2d} standard deviations from the mean. This represents {2} gross revenue potential.'.format(
        value, standard_deviation, get_summary_qualifier_by_standard_deviation(standard_deviation)
    )


def get_average_summary_by_standard_deviation(value, standard_deviation):
    """
    Get the per capita potential summary based on the input range the standard deviation falls into.
    :param value:
    :param standard_deviation:
    :return: The summary explanation describing what the value means.
    """
    # create the statement
    return 'The potential for per capita, or per customer sales is {0:,0f} dollars, {1:,2d} standard deviations from the mean. This represents {2} per capita revenue potential.'.format(
        value, standard_deviation, get_summary_qualifier_by_standard_deviation(standard_deviation)
    )


def get_combined_summary(gross_standard_deviation, average_standard_deviation):
    """
    Get the combined summary based on the
    :param gross_standard_deviation:
    :param average_standard_deviation:
    :return:
    """
    # calculate a combined metric
    gross = int(math.floor(gross_standard_deviation))
    average = int(math.floor(average_standard_deviation))
    combined = gross + average

    # create a lookup matrix based on the combined metric
    combined_lookup = {
        6: 'very exceptional',
        5: 'exceptional',
        4: 'very strong',
        3: 'strong',
        2: 'good',
        1: 'above average',
        0: 'average',
        -1: 'below average',
        -2: 'sub par',
        -3: 'weak',
        -4: 'very weak',
        -5: 'poor',
        -6: 'very poor'
    }

    # return the combined summary statement
    return 'Taking into consideration both the gross, and per capita sales potential, this area possesses {0} revenue potential.'.format(
        combined_lookup[combined]
    )


def get_full_summary(gross_value, gross_standard_deviation, average_value, average_standard_deviation):
    """
    Get the full summary statement string.
    :param gross_value:
    :param gross_standard_deviation:
    :param average_value:
    :param average_standard_deviation:
    :return:
    """
    # create a list of all the statements
    summary_list = [
        get_combined_summary(gross_standard_deviation, average_standard_deviation),
        get_gross_summary_by_standard_deviation(gross_value, gross_standard_deviation),
        get_average_summary_by_standard_deviation(average_value, average_standard_deviation)
    ]

    # combine and return the result as one single string
    return ' '.join(summary_list)


def calculate_summary_field(input_table, gross_value_field, average_value_field, summary_field):
    """
    Calculate the full summary based on a value and standard deviations for both gross and per capita revenue.
    :param input_table:
    :param gross_value_field:
    :param average_value_field:
    :param summary_field:
    :return:
    """
    # if the summary field does not already exist
    if not len(arcpy.ListFields(input_table, summary_field)):

        # create the summary field
        arcpy.AddField_management(
            in_table=input_table,
            field_name=summary_field,
            field_alias='Summary',
            field_type='TEXT',
            field_length=2500
        )

    # calculate the respective standard deviations
    value_list = [r for r in arcpy.da.SearchCursor(input_table, (gross_value_field, average_value_field))]
    gross_standard_deviation = math.stdev([value[0] for value in value_list])
    average_standard_deviation = math.stdev(value[1] for value in value_list)

    # create an update cursor to manipulate the table
    with arcpy.da.UpdateCursor(input_table, [gross_value_field, average_value_field, summary_field]) as update_cursor:

        # iterate the rows
        for row in update_cursor:

            # get the full summary
            row[2] = get_full_summary(row[0], gross_standard_deviation, row[1], average_standard_deviation)

            # push the update
            update_cursor.updateRow(row)
