def pd_clean_col(mediumDF):
    """
        Removes dublicate columns such as bookmarkedat, posturl, posttitle.
        Checks if there is some unexpected condition

        Returns
        -------
        `pandas.core.frame.DataFrame` object : Cleaned Dataframe
    """
    old_c_names = mediumDF.columns.values.tolist()  # Get the list of column names
    mediumDF = mediumDF[["bookmarked_at", "post_url" ,"post_title"]]  # Select Specific Columns
    new_c_names = mediumDF.columns.values.tolist() # Get the list of column names again

    # insensitive to order but sensitive to occurence
    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

    if not compare(old_c_names, new_c_names):
        expanded_c_names = []
        for i in new_c_names:
            expanded_c_names.append(i)
            if("_" in i):
                expanded_c_names.append(i.replace("_", ""))



        if args.verbose:
            print("\nBefore Column Cleaning: ", old_c_names, "\nAfter Column Cleaning: ", new_c_names, "\nCleaned Column Expanded: ", expanded_c_names)



        if compare(old_c_names, expanded_c_names):
            if args.verbose:
                print("DataFrame Cleaned")
        else: print("Opps, Expanded Column list doesn't match the uncleaned list!")

    else:
        print("Opps, Something went wrong in DataFrame Column Cleaning!")

    return mediumDF
