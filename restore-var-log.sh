# Restore tmpfs directories for logs. 
# Extend the following directories to your needs according to installed packages
for dir in apparmor apt cups dist-upgrade fsck gdm3 hp installer speech-dispatcher samba unattended-upgrades ;
do
  if [ ! -e /var/log/$dir ] ; then
    mkdir /var/log/$dir
  fi
done

# Restore syslog files
for file in debug mail.err mail.log mail.warn syslog ;
do
  if [ ! -f /var/log/$file ] ; then
    touch /var/log/$file
    chown syslog:adm /var/log/$file
  fi
done

# Set owners for the newly created log directories
chown root:lp /var/log/cups
chown root:gdm /var/log/gdm3
chown root:adm /var/log/samba
