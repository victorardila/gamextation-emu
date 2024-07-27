import configparser
import os

class StorageSystem:
    
    BG_COLOR_DARK = (
        "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(34, 34, 34, 255), stop:0.5 rgba(40, 40, 40, 255), "
        "stop:0.75 rgba(50, 50, 50, 255), stop:1 rgba(34, 34, 34, 255));"
    )
    BG_COLOR_LIGHT = (
        "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
        "stop:0.026178 rgba(249, 135, 11, 255), stop:0.219895 rgba(247, 134, 12, 255), "
        "stop:0.424084 rgba(241, 139, 11, 255), stop:0.715789 rgba(233, 150, 10, 255), "
        "stop:0.826316 rgba(232, 155, 13, 255), stop:1 rgba(235, 154, 11, 255));"
    )
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

    def create_config(self, settings):
        """
        Create a new configuration file with the provided settings.
        :param settings: A dictionary containing the settings to be saved.
        """
        for section, options in settings.items():
            if 'theme' in options and options['theme'] == 'light':
                options['bg_color'] = self.BG_COLOR_LIGHT
        self.config.read_dict(settings)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def read_config(self):
        """
        Read the configuration file.
        :return: A dictionary containing the settings.
        """
        if not os.path.exists(self.config_file):
            return {}
        self.config.read(self.config_file)
        settings = {}
        for section in self.config.sections():
            settings[section] = dict(self.config.items(section))
        return settings

    def update_config(self, section, option, value):
        """
        Update a specific setting in the configuration file.
        :param section: The section in which the option is located.
        :param option: The option to be updated.
        :param value: The new value for the option.
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        if option == 'theme':
            bg_color = self.BG_COLOR_DARK if value == 'dark' else self.BG_COLOR_LIGHT
            self.config.set(section, 'bg_color', bg_color)
        self.config.set(section, option, value)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def delete_config(self):
        """
        Delete the configuration file.
        """
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def delete_section(self, section):
        """
        Delete a specific section from the configuration file.
        :param section: The section to be deleted.
        """
        if self.config.has_section(section):
            self.config.remove_section(section)
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)

    def delete_option(self, section, option):
        """
        Delete a specific option from a section in the configuration file.
        :param section: The section in which the option is located.
        :param option: The option to be deleted.
        """
        if self.config.has_section(section) and self.config.has_option(section, option):
            self.config.remove_option(section, option)
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
    
    def get_option(self, section, option):
        """
        Get the value of a specific option in a section.
        :param section: The section in which the option is located.
        :param option: The option to get the value from.
        :return: The value of the option.
        """
        if self.config.has_section(section) and self.config.has_option(section, option):
            return self.config.get(section, option)
        return None