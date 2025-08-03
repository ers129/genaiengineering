import pandas as pd

def get_toppers(csv_file_path):
    
    subject_list = ['Math', 'Science', 'English']

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # print (df.dtypes)

    # Apply eligibility criteria
    eligible = df[(df['Attendance (%)'] >= 60.0) & (df['Project Submitted'])]

    # Initialize dictionary to store results
    result = {'Subject Toppers': {}, 'Overall Topper(s)': []}

    # Identify subject-wise toppers
    for subject in subject_list:
        max_score = eligible[subject].max()
        toppers = eligible[eligible[subject] == max_score]['Name'].tolist()
        result['Subject Toppers'][subject] = toppers

    # Overall toppers (based on average of subjects)
    # Average calcultion
    eligible['Average'] = eligible[subject_list].mean(axis=1)
    
    # Max mark
    max_total = eligible['Average'].max()
    overall_toppers = eligible[eligible['Average'] == max_total]['Name'].tolist()
    result['Overall Topper(s)'] = overall_toppers

    return result

def additional_data(csv_file_path):
    
    # Read CSV
    df = pd.read_csv(csv_file_path)

    subject_list = ['Math', 'Science', 'English']

    # Compute Average Score
    df['Average Score'] = df[subject_list].mean(axis=1)

    # funnction to assign Grade based on average score
    def assign_grade(avg):
        if avg >= 90:
            return 'A'
        elif avg >= 75:
            return 'B'
        elif avg >= 60:
            return 'C'
        else:
            return 'D'

    # Apply function based on average marks column
    df['Grade'] = df['Average Score'].apply(assign_grade)

    # Functiion to assign Performance: multiple info from the row
    def assign_performance(row):
        if row['Grade'] == 'A' and row['Attendance (%)'] > 90 and row['Project Submitted']:
            return 'Excellent'
        elif row['Grade'] == 'D' or row['Attendance (%)'] < 60 or not row['Project Submitted']:
            return 'Needs Attention'
        else:
            return 'Satisfactory'

    # Each row passed as argument
    df['Performance'] = df.apply(assign_performance, axis=1)

    return df

import pandas as pd

def export_summary_statistics(data_file, output_csv_path):
    # Read the data
    df = pd.read_csv(data_file)

    # Select relevant columns
    cols_reqd = ['Math', 'Science', 'English', 'Attendance (%)']
    summary = df[cols_reqd].describe()

    # Export summary to CSV
    summary.to_csv(output_csv_path)


# File Name
data_file = 'student_scores.csv'

# Get the topper list
toppers = get_toppers (data_file)
print (toppers)

# Get the data frame with additional columns
df_additional_data = additional_data (data_file)
print (df_additional_data)
# df_additional_data.to_csv ('Temp.csv', index=False, float_format="%.2f")

# Summary stat
export_summary_statistics (data_file, 'Summary_Stat.csv')
