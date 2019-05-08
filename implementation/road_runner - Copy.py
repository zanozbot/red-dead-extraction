# In order for this program to work we assume that the HTML code complies to the XHTML specification
# #!/usr/bin/env python

from bs4 import BeautifulSoup


def is_tag(line):
    return ('<' in line) and ('>' in line)


def is_end_tag(line):
    return ('</' in line)


def same_line(wrapper_line, sample_line):
    return wrapper_line == sample_line


def is_text(line):
    return not is_tag(line)


def tag_name(line):
    return line.replace('<', '').replace('>', '').replace('/', '').split()[0]


def tag_to_optional(sample, tag_name, index):
    tag = sample.findAll(tag_name)[index].prettify().strip()
    tag_length = len([line.strip() for line in tag.split('\n')])
    return tag_length, "(" + str(tag) + ")?"


def is_optional_on_sample(wrapper_lines, sample_lines, wrapper, sample, tag_name, tag_index, wrapper_index, sample_index):
    tag = sample.findAll(tag_name)[tag_index].prettify().strip()
    tag_length = len([line.strip() for line in tag.split('\n')])
    if (sample_index + tag_length > len(sample_lines)):
        return False
    elif (wrapper_index + tag_length > len(wrapper_lines)):
        return True
    return wrapper_lines[wrapper_index] == sample_lines[sample_index + tag_length]


def is_iterator(sample_lines, sample, tag_name, tag_index, line_index):
    if(tag_index == 0):
        return False

    tag = sample.findAll(tag_name)[tag_index].prettify().strip()
    tag_length = len([line.strip() for line in tag.split('\n')])
    return sample_lines[line_index-tag_length] == sample_lines[line_index] and sample_lines[line_index+tag_length-1] == sample_lines[line_index-1]


def get_iterator(sample_lines, sample, tag_name, tag_index, line_index):
    tag = sample.findAll(tag_name)[tag_index].prettify().strip()
    for index, line in enumerate(tag, start=0):
        if(not same_line(line, sample_lines[index + line_index]) and is_text(line)):
            tag[index] = "#PCDATA"
    tag_length = len([line.strip() for line in tag.split('\n')])
    return tag_length, [line.strip() for line in tag.split('\n')]


def tag_to_iterator(tag):
    tag[0] = "(" + tag[0]
    tag[-1] = tag[-1] + ")+"
    return tag


def remove_previous_iterator_occurances(wrapper, iterator_lines, iterator_length):
  # TODO: REMOVE even if ()?+
    while (wrapper[-iterator_length] == iterator_lines[0] and wrapper[-1] == iterator_lines[-1]):
        for i in range(iterator_length):
            print("DELETING: " + wrapper[-1])
            del wrapper[-1]
    return True


# Takes a wrapper file and a sample file. Returns a more generalized wrapper
def generalize(wrapper_location, sample_location):
    wrapper = BeautifulSoup(open(wrapper_location), "html.parser")
    sample = BeautifulSoup(open(sample_location), "html.parser")

    new_wrapper = []
    # Keeps track of what tag we're currently at
    sample_tag_count = {}
    wrapper_tag_count = {}

    wrapper_lines = [line.strip() for line in wrapper.prettify().split('\n')]
    sample_lines = [line.strip() for line in sample.prettify().split('\n')]
    skip_line = 0
    wrapper_index = 0
    sample_index = 0
    previous_wrapper_index = -1
    previous_sample_index = -1

    while (sample_index < len(sample_lines)):
        # Increment tag counter
        if is_tag(sample_lines[sample_index]) and not is_end_tag(sample_lines[sample_index]) and previous_sample_index != sample_index:
            if(tag_name(sample_lines[sample_index]) in sample_tag_count):
                sample_tag_count[tag_name(sample_lines[sample_index])] += 1
            else:
                sample_tag_count[tag_name(sample_lines[sample_index])] = 0
            previous_sample_index = sample_index
        if is_tag(wrapper_lines[wrapper_index]) and not is_end_tag(wrapper_lines[wrapper_index]) and previous_wrapper_index != wrapper_index:
            if(tag_name(wrapper_lines[wrapper_index]) in wrapper_tag_count):
                wrapper_tag_count[tag_name(wrapper_lines[wrapper_index])] += 1
            else:
                wrapper_tag_count[tag_name(wrapper_lines[wrapper_index])] = 0
            previous_wrapper_index = wrapper_index

        # Same line - do nothing
        if (same_line(wrapper_lines[wrapper_index], sample_lines[sample_index])):
            print(sample_lines[sample_index])
            new_wrapper.append(sample_lines[sample_index])
            wrapper_index += 1
            sample_index += 1

        # Different text - #PCDATA
        elif (is_text(sample_lines[sample_index])):
            print("#PCDATA")
            new_wrapper.append("#PCDATA")
            wrapper_index += 1
            sample_index += 1

        # Different tags - check for iterations and optionals
        else:
            iterator_check = False

            # Iterations
            if(is_iterator(sample_lines, sample, tag_name(sample_lines[sample_index]), sample_tag_count[tag_name(sample_lines[sample_index])], sample_index)):
                tag_length, tag = get_iterator(sample_lines, sample, tag_name(
                    sample_lines[sample_index]), sample_tag_count[tag_name(sample_lines[sample_index])], sample_index)
                remove_previous_iterator_occurances(
                    new_wrapper, tag, tag_length)
                sample_index += tag_length

                for line in tag_to_iterator(tag):
                    new_wrapper.append(line)
                iterator_check = True
            if(is_iterator(wrapper_lines, wrapper, tag_name(wrapper_lines[wrapper_index]), wrapper_tag_count[tag_name(wrapper_lines[wrapper_index])], wrapper_index)):
                tag_length, tag = get_iterator(wrapper_lines, wrapper, tag_name(
                    wrapper_lines[sample_index]), wrapper_tag_count[tag_name(wrapper_lines[wrapper_index])], wrapper_index)
                remove_previous_iterator_occurances(
                    new_wrapper, tag, tag_length)
                wrapper_index += tag_length
                for line in tag_to_iterator(tag):
                    new_wrapper.append(line)
                iterator_check = True

            # Optionals
            if(not iterator_check):
                if(is_optional_on_sample(wrapper_lines, sample_lines, wrapper, sample, tag_name(sample_lines[sample_index]), sample_tag_count[tag_name(sample_lines[sample_index])], wrapper_index, sample_index)):
                    tag_length, tag_optional = tag_to_optional(sample, tag_name(
                        sample_lines[sample_index]), sample_tag_count[tag_name(sample_lines[sample_index])])
                    sample_index += tag_length
                    for line in tag_optional.split('/n'):
                        new_wrapper.append(line)
                    print(tag_optional)
                else:
                    # print(wrapper_tag_count)
                    tag_length, tag_optional = tag_to_optional(wrapper, tag_name(
                        wrapper_lines[wrapper_index]), wrapper_tag_count[tag_name(wrapper_lines[wrapper_index])])
                    wrapper_index += tag_length
                    for line in tag_optional.split('/n'):
                        new_wrapper.append(line)
                    print(tag_optional)

    print("## FINAL WRAPPER ##")
    for line in new_wrapper:
        print(line)


generalize('../input/road_runner/siteA.html',
           '../input/road_runner/siteB.html')
