# Creating a Linux Virtual Machine in Windows

Here are instructions to install and run a Linux virtual machine in Windows, using the VMware Workstation Player for Windows and CentOS Stream 9. This setup will allow you to write and run the Ansible playbooks in the tutorial. Once again, this is not the only way to create and use a Linux environment in Windows, but reviewing all the options is beyond the scope of this tutorial.

- [Download CentOS](#download-centos)
- [Install VMware Workstation Player for Windows](#install-vmware-workstation-player-for-windows)
- [Create a Virtual Machine](#create-a-virtual-machine)
- [Setup CentOS](#setup-centos)
- [Login and Update the System](#login-and-update-the-system)

-----

## Download CentOS

***CentOS Stream*** is a Fedora-family Linux distribution. It is a free and open-source midstream distribution between community-supported Fedora Linux distributions and commercial Red Hat Enterprise Linux (RHEL) distributions.

1. Go to <https://www.centos.org/>.

    ![The CentOS Project](img/install_01.png)

2. Click on the **Downloads** link.

    ![CentOS Downloads](img/install_02.png)

3. Click on the **CentOS Stream** tab.

    ![CentOS Stream Download](img/install_03.png)

4. Select the latest version of CentOS Stream, then click on the **x86_64** architecture link. Wait until your browser completes the download, then open your **Downloads** folder. Check that the download was successful.

    ![Downloads folder](img/install_04.png)

    > **NOTE** - By default, browsers will download the disk image to your **Downloads** folder. However, if you prefer not to use that folder for long-term storage, you can move the image to another location. Just remember the location, so you can enter it into VirtualBox later on.

-----

## Install VMware Workstation Player for Windows

***VMware Workstation Player*** is a Type-2 Hypervisor that can run virtual machines and appliances on multiple operating systems, including Windows.

At the time of this writing, the latest version of Workstation Player, version 17, is compatible with Windows 8.1 and Windows Server 2012 or later. However, you should use the VMware Compatibility Guide at <https://www.vmware.com/resources/compatibility/search.php> to ensure you use the version of Workstation Player that is compatible with your version of Windows.

1. Go to <https://www.vmware.com>.

    ![VMware](img/install_05.png)

2. Click on the **Products** tab and select **Workstation Player**. You may also navigate directory to <https://www.vmware.com/products/workstation-player.html>

    ![Workstation Product Link](img/install_06.png)

3. Click on the **DOWNLOAD FOR FREE** link.

    ![VMware Workstation Player](img/install_07.png)

4. A new tab or window will open. Ensure you select the latest version, then click on **GO TO DOWNLOADS**.

    ![Download VMware Workstation Player](img/install_08.png)

5. Click on the **Download** button that corresponds to **VMware Workstation 17.5.0 Player for Windows 64-bit Operating Systems**.

    ![Download Product](img/install_09.png)

6. Wait until your browser completes the download, then open your **Downloads** folder. Right-click on the downloaded file and select **Run as administrator**.

   ![Downloads folder](img/install_10.png)

7. If your system's User Account Control asks, ***"Do you want to allow this app to make changes to your device?"***, click on **Yes**.

   ![User Account Control](img/install_11.png)

8. When the ***Welcome to the VMware Workstation 17 Player Setup Wizard*** dialog appears, click on **Next**.

   ![VMware Workstation 17 Player Setup](img/install_12.png)

9. The End-User License Agreement (EULA) will appear. Once you have finished reading it, check **I accept the terms in the License Agreement** and click on **Next**.

   ![VMware EULA](img/install_13.png)

10. The **Custom Setup** dialog should appear.

    ![Custom Setup](img/install_14.png)

    - **Install to:** - The first item is the location of the VMware executables; the default value should work on your system.
    - **Enhanced Keyboard Driver** - This feature allows you to use key combinations, such as **[Ctrl]** + **[Alt]** + **[Del]** or **[Win]** + **[L]**, within the virtual machine without being intercepted by the Windows host operating system. It also allows to use additional features on international and non-standard keyboards. You will not use any special key combinations or require any special keyboard features in the tutorial, so you can leave this unchecked.
    - **Add VMware Workstation console tools into system PATH** - This option allows you to run VMware command-line interface (CLI) commands, such as **vmrun**, without having to prepend the path to the VMware executables. You can leave this checked, but you will not be using any console commands in the tutorial.

    Click **Next** to continue.

11. The **User Experience Settings** dialog should appear.

    ![User Experience Settings](img/install_15.png)

    - Leave **Check for product updates on startup** checked to ensure the application is up-to-date.
    - If you would like to **Join the VMware Customer Experience Improvement Program**, leave this checked. However, you do not need to join the program to perform the tasks in the tutorial.

12. The **Shortcuts** dialog should appear. Leaving both options checked will make accessing your virtual machine easier.

    ![Shortcuts](img/install_16.png)

13. When the **Ready to install VMware Workstation 17 Player** dialog appears, click on **Install**.

    ![Ready to install VMware Workstation 17 Player](img/install_16.png)

14. The wizard will start installing VMware Workstation 17 Player.

    ![Installation Progress](img/install_18.png)

15. Click on **Finish** when the wizard tells you the installation is complete.

    ![Installation Complete](img/install_19.png)

16. Go back to your Desktop. Click on the Workstation icon or select **All Apps** -> **VMware** -> **VMware Workstation 17 Player** from you application menu.

    ![Workstation Player Icon](img/install_20.png)

17. When VMware Workstation 17 Player starts, select **Use VMware Workstation 17 Player for free for non-commercial use** and click on **Continue**.

    ![Welcome to VMware Workstation 17 Player](img/install_21.png)

18. At the next dialog windows, click on **Finish**.

    ![Thank you for using VMware Workstation 17 Player](img/install_22.png)

-----

## Create a Virtual Machine

1. When the VMware Workstation 17 Player welcome dialog appears, select **Create a New Virtual Machine**.

    ![Welcome to VMware Workstation 17 Player](img/install_23.png)

2. The **Welcome to the New Virtual Machine Wizard** dialog should appear. Select **I will install the operating system later** and click on **Next**.

   ![Welcome to the New Virtual Machine Wizard](img/install_24.png)

3. When the **Select a Guest Operating System** dialog appears, select **Linux** and select **Red Hat Enterprise Linux 9 64-bit** for the version (there is no option for CentOS 9). Click on **Next** when you are finished.

   ![Select a Guest Operating System](img/install_25.png)

4. When the **Name the Virtual Machine** dialog appears, enter the following information.

   ![Name the Virtual Machine](img/install_26.png)

   - **Virtual machine name:** *a4p*
   - **Location:** By default, VMware will create the virtual machine in your Documents folder. You can change this location if you wish.

   Click **Next** when you have finished filling out the text boxes.

5. When the **Specify Disk Capacity** dialog appears, enter the following information.

   ![Specify Disk Capacity](img/install_27.png)

   - **Maximum disk size (GB):** *20*
   - Select **Split virtual disk into multiple files**

6. When the **Ready to Create Virtual Machine** dialog appears, click on **Customize Hardware...**.

   ![Ready to Create Virtual Machine](img/install_28.png)

7. When the **Hardware** dialog appears, ensure that you allocate at least 2048 MB of memory and 2 processors. Once set, click on **New CD/DVD (SATA)**.

    ![Hardware - RAM and Cores](img/install_29.png)

8. Select **Use ISO image file** and click on **Browse...**.

   ![Hardware - CD/DVD](img/install_30.png)

9. An Explorer dialog window should appear. Navigate to where you stored your disk image and select it.

   ![Browse for ISO Image](img/install_31.png)

10. When you return to the **Hardware** dialog, click on **Close**.

    ![Hardware - All Set](img/install_32.png)

11. When you return to the **Ready to Create Virtual Machine** dialog, make sure the information is correct, then click **Finish**.

    ![Create Virtual Machine](img/install_33.png)

-----

## Setup CentOS

1. At the main dialog, click on **Play virtual machine**.

    ![Play virtual machine](img/install_34.png)

2. The GRUB menu will appear. Click inside the window; it will capture your mouse cursor. Select **Install CentOS Stream 9**, then press **[Ctrl]** + **[Alt]** to release the mouse cursor.

   ![GRUB Menu](img/install_35.png)

3. Wait for the installation wizard to start. When the **Welcome to CentOS Stream 9** screen appears, select your language and click on **Continue**.

   ![Welcome to CentOS Stream 9](img/install_36.png)

4. The **Installation Summary** should appear.

   ![Installation Summary](img/install_37.png)

5. Under **System**, select **Installation Destination**. When the screen appears, ensure the 20 GiB VMware Virtual Disk is selected and checked, then click on **Done**.

   ![Installation Destination](img/install_38.png)

6. When you return to the **Installation Summary**, under **User Settings**, click on **Root Password**. Enter the following information:

   ![Root Password](img/install_39.png)

   - **Root Password** - Enter a password of your choice. By the way, if the password is weak or fails a dictionary check, the wizard will warn you that you will have to click on **Done** twice to use the password.
   - **Confirm** - Re-enter the password you chose.
   - **Lock root account** - Unchecked
   - **Allow root SSH login with password** - Unchecked

   Click on **Done** when finished.

7. When you return to the **Installation Summary**, under **User Settings**, click on **User Creation**. Enter the following information:

   ![User Creation](img/install_40.png)

   - **Full name** - *a4puser*
   - **User name** - *a4puser*
   - **Make this user administrator** - Checked
   - **Require a password to use this account** - Checked
   - **Password** - Enter a password of your choice. By the way, if the password is weak or fails a dictionary check, the wizard will warn you that you will have to click on **Done** twice to use the password.
   - **Confirm password** - Re-enter the password you chose.

   Click on **Done** when finished.

8. When you return to the **Installation Summary**, click on **Begin Installation**. The installation will start.

   ![Installation Progress](img/install_41.png)

9. Once the installation is complete, click on **Reboot System**.

   ![Reboot System](img/install_42.png)

-----

## Login and Update the System

1. Once the system has finished rebooting, click on **a4puser**:

    ![CentOS Lock Screen](img/install_43.png)

2. Enter your password in the text box and press **[Enter]**:

   ![CentOS Login](img/install_44.png)

3. When the **Welcome to CentOS** dialog appears, you can take the tour or decline:

   ![Welcome to CentOS](img/install_45.png)

4. When you return to the main screen, click on **Activities** at the top of the screen, and then click on the **Terminal** icon at the bottom of the screen.

   ![Open a Terminal](img/install_46.png)

5. The Terminal window will open:

   ![The Terminal](img/install_47.png)

6. At the prompt, enter the following commands to ensure your system is up-to-date:

   ```bash
   sudo dnf -y update
   ```

7. Enter your password when prompted:

   ![Updating the system](img/install_49.png)

8. Once the `update` command is complete, enter the following commands at the prompt to check for upgrades and remove any packages that are no longer required.

   ```
   sudo dnf -y upgrade
   sudo dnf -y autoremove
   ```

That's it! Now you have a Linux distribution ready to use with the tutorial. Good luck!
