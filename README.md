[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/u8FyG16T)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=16698345)

# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: [Inconsistent]
- **Columns**: [income_groups, age, gender, year, population]

### Column Details
| Column Name    | Data Type | Non-Null Count |    Mean    |  Unique Values  |
|----------------|-----------|----------------|------------|-----------------|
| income_groups  | object    | 119412         | ...        |        8        |
| age            | float64   | 119495         | 50.01      |       ...       |
| gender         | float64   | 119811         | 1.58       |      1,2,3      |
| year           | object    | 125718         | 2025.07    |       ...       |
| population     | object    | 125718         | 1.11e+08   |       ...       |


### Identified Issues

1. **There are many null values in the age, gender, income_groups columns** 
    If uncleaned, aggregate analysis of individual columns might be off, and column-wise operations 
    may mismatch due to different column lengths

```python
print(df_messy.isnull().sum())

income_groups   | 6306
age             | 6223
gender          | 5907
year            | 0
population      | 0
```

2. **The NAs lead to different column lengths**  
   The variable types don't really make sense. For example, `age` and `gender` shouldn't be floats, while `year` and `population` should be integers. This will affect any sort of mathematical analysis we do if we don't know the variable types, such as rounding errors and iterating.
   We also can't perform many functions on variables of `object` type (i.e., `df.describe()` doesn't work on object columns).


```plaintext
Sample of messy data:
             income_groups   age  gender    year  population
88554  lower_middle_income  90.0     1.0  2018.0    251902.0
8328           high_income   NaN     2.0  1973.0   5885911.0
48368           low_income  61.0     1.0  1998.0    756458.0
77021  lower_middle_income  56.0     1.0  1961.0   2879008.0
86215  lower_middle_income  83.0     1.0  2095.0  13659410.0
47899           low_income   6.0     2.0  1982.0   4042516.0
22530          high_income  75.0     3.0  1981.0   2953274.0
55462           low_income  82.0     2.0  1995.0    111263.0
38430           low_income  31.0     1.0  2026.0   6315439.0
29405          high_income  96.0     1.0     nan    890697.0
```

3.  **Logical errors** 
    Using year as an example, after casting to float/int, we can then use describe to check the
    min/max/mean/percentiles. However, we notice that there are logical errors such as a maximum 
    year of 2119, which doesn't make sense. The same can probably be seen in the other variables. 
    This may affect the plausibility of any analysis we do in the future.

```python
print((df_messy.year).astype(float).describe())
```
```plaintext
count    119516.000000
mean       2025.068049
std          43.584951
min        1950.000000
25%        1987.000000
50%        2025.000000
75%        2063.000000
max        2119.000000
Name: year, dtype: float64
```

4. **The messy data has 2950 duplicated rows**
    This is just purely unnecessary and adds no value to the data and especially analysis. It may 
    overcount for analysis.
    
```python
print(df_messy[df_messy.duplicated()])
```
```plaintext
              income_groups   age  gender    year  population
1254            high_income  11.0     1.0     nan         nan
7082            high_income   NaN     1.0  2086.0         nan
9556            high_income  36.0     2.0     nan         nan
15820           high_income  55.0     1.0     nan         nan
18629           high_income   NaN     2.0     nan         nan
...                     ...   ...     ...     ...         ...
125661  upper_middle_income  85.0     1.0  1962.0    120531.0
125662  upper_middle_income  57.0     2.0  1960.0   4199195.0
125663           low_income   8.0     1.0  2098.0  17221330.0
125664                  NaN  99.0     1.0     nan     10101.0
125665  upper_middle_income  80.0     1.0  2014.0   2887365.0
```

### 2. Data Cleaning Process

### original

```plaintext
Data columns (total 5 columns):
     Column         Non-Null Count   Dtype  
---  ------         --------------   -----  
 0   income_groups  119412 non-null  object 
 1   age            119495 non-null  float64
 2   gender         119811 non-null  float64
 3   year           119516 non-null  float64
 4   population     119378 non-null  float64
dtypes: float64(4), object(1)
```

### dropping NAs...

```plaintext
Data columns (total 5 columns):
     Column         Non-Null Count  Dtype  
---  ------         --------------  -----  
 0   income_groups  97639 non-null  object 
 1   age            97639 non-null  float64
 2   gender         97639 non-null  float64
 3   year           97639 non-null  float64
 4   population     97639 non-null  float64
dtypes: float64(4), object(1)
```
### dropping duplicates, changing datatypes

```plaintext
                age        gender          year    population
count  95425.000000  95425.000000  95425.000000  9.542500e+04
mean      50.033440      1.581252   2025.108577  1.136237e+08
std       29.154717      0.592209     43.565393  1.278529e+09
min        0.000000      1.000000   1950.000000  2.200000e+01
25%       25.000000      1.000000   1987.000000  2.315926e+06
50%       50.000000      2.000000   2025.000000  7.157996e+06
75%       75.000000      2.000000   2063.000000  1.471034e+07
max      100.000000      3.000000   2119.000000  3.293043e+10
```

### dropping bogus values in year (48141 rows) and gender (5120 rows) 


```plaintext
                age        gender          year    population
count  44771.000000  44771.000000  44771.000000  4.477100e+04
mean      50.002680      1.500704   1987.028568  8.781311e+07
std       29.180723      0.500005     21.629073  1.045830e+09
min        0.000000      1.000000   1950.000000  2.200000e+01
25%       25.000000      1.000000   1968.000000  8.560390e+05
50%       50.000000      2.000000   1987.000000  4.430533e+06
75%       75.000000      2.000000   2006.000000  8.400894e+06
max      100.000000      2.000000   2024.000000  3.293043e+10
```

### dropping outliers in population (897 rows), the population distribution is more normal

```plaintext
                age        gender          year    population
count  43874.000000  43874.000000  43874.000000  4.387400e+04
mean      49.685531      1.502006   1987.156197  9.816549e+06
std       28.936015      0.500002     21.623516  4.408226e+07
min        0.000000      1.000000   1950.000000  6.420000e+02
25%       25.000000      1.000000   1968.000000  9.008068e+05
50%       50.000000      2.000000   1987.000000  4.430620e+06
75%       75.000000      2.000000   2006.000000  8.313851e+06
max      100.000000      2.000000   2024.000000  9.110961e+08
```

## 3. Final State Analysis

- **Name**: cleaned_population_data.csv
- **Rows**: [43874]
- **Columns**: [income_groups, age, gender, year, population]

### Column Details
| Column Name    | Data Type | Non-Null Count |    Mean    |  Unique Values  |
|----------------|-----------|----------------|------------|-----------------|
| income_groups  | object    | 43874          | ...        |        8        |
| age            | int       | 43874          | 49.67      |       ...       |
| gender         | int       | 43874          | 1.5        |       1,2       |
| year           | int       | 43874          | 1987.16    |       ...       |
| population     | int       | 43874          | 9.81+e06   |       ...       |


### Original cleaned df for comparison

```plaintext
                 age         gender           year    population
count  122008.000000  122008.000000  122008.000000  1.220080e+05
mean       50.000000       1.500000    2025.000000  9.235068e+06
std        29.154879       0.500002      43.589168  8.492751e+06
min         0.000000       1.000000    1950.000000  2.100000e+01
25%        25.000000       1.000000    1987.000000  2.221932e+06
50%        50.000000       1.500000    2025.000000  7.042608e+06
75%        75.000000       2.000000    2063.000000  1.392130e+07
max       100.000000       2.000000    2100.000000  3.432180e+07
```

### Summary of changes

The number of rows cut down by over 50%. There are no NaN values in any rows. 
Gender is now 1 or 2, the number of years is now maxed at 2024, the population is within reasonable 
range without outliers. I made assumptions by looking at the cleaned dataset for datatypes and also 
the dirty-data.py to see what kind of altercations were made for the dirty data. I tried to undo 
those step by step; however this resulted in a severe cut-down of data observations. The original 
clean dataset had 122008 entries for all features, but now the new cleaned dataset set only has 
43874 observations. There weren't super significant challenges other than figuring out what made
the dirty dataset 'dirty' and checking my cleaned dataset was, in fact, 'clean.' The only method I 
had look up was how to get rid outliers for the population (I used stackoverflow for quantiles). I 
also learned how to use shorthand methods to quickly analyze a dataset and point out what might be 
inconsistent to work with (it's always good to check for NaNs, dupes, datatypes, and outliers). But, 
in turn, there is a trade off with having quality data but also enough data. In the future, I may 
consider being more conservative in data processing, so I will not lose any important information 
that could have come from the messy data. 

Comparing the results from cleaning and the original clean df, I was more robust in restricting the
years to be <=2024 when the original had a maximum of 2100. The original population is more narrow
in its range, while mine may have been too conservative in ridding outliers. The gender distribution
is about the same, and the age is about the same as well. 

